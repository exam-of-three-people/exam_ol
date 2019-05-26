from flask import render_template, redirect, flash, url_for, request, json, session
from forms import LoginForm, RegisterFormStudent, RegisterFormTeacher, StudentInfoForm, TeacherInfoForm, TestCreaterForm
from models import app, Student, Teacher, College, Major, StudentSubject, TeacherSS, Subject, Page, Test, Class, db
from sqlalchemy.exc import IntegrityError, InternalError
from sqlalchemy import func
import time, json, datetime


@app.route("/", methods=['GET', 'POST'])
@app.route("/index", methods=['GET', 'POST'])
@app.route("/login", methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        form = LoginForm(request.form)
        if form.validate_on_submit():
            id = int(form.id.data)
            password = form.password.data
            if form.role.data == 1:
                user = Student.query.get(id)
                if user is None:
                    flash("学号输入错误！")
                elif user.checkPassword(password):
                    session["is_login"] = True
                    session["uid"] = user.id
                    session["role"] = "student"
                    return redirect("studentMenu")
                else:
                    flash("密码不正确！")
            elif form.role.data == 2:
                user = Teacher.query.get(id)
                if user is None:
                    flash("工号输入错误！")
                elif user.checkPassword(password):
                    session["is_login"] = True
                    session["uid"] = user.id
                    session["role"] = "teacher"
                    return redirect("teacherMenu")
                else:
                    flash("密码不正确！")
                    pass
                pass
            pass
        else:

            pass
    else:
        # noinspection PyBroadException
        try:
            if session["is_login"]:
                flash("你已经登录，无需重复登录！")
                return redirect(session["role"] + "Menu")
        except Exception:
            pass
    form = LoginForm()
    return render_template("登录页面_B.html", form=form)


@app.route("/studentMenu", methods=['GET', 'POST'])
def studentMenu():
    student = Student.query.get(session["uid"])
    now = datetime.datetime.now()
    pages = student.get_pages()
    pages_show = []
    for page in pages:
        # 已经参加过的考试不再显示
        if not page.finshed and page.date == now.date():
            pages_show.append(page)
    return render_template("学生菜单_B.html", pages=pages_show)


@app.route("/teacherMenu", methods=['GET', 'POST'])
def teacherMenu():
    return redirect('/testCreater')


@app.route("/adminMenu", methods=['GET', 'POST'])
def adminMenu():
    return render_template("管理员菜单.html")


@app.route("/teacherManager", methods=['GET', 'POST'])
def teacherManager():
    return render_template("教师管理页面.html")


@app.route('/studentManager', methods=['GET', 'POST'])
def studentManager():
    return render_template("学生管理页面.html")


@app.route('/testManager', methods=['GET', 'POST'])
def testManager():
    return render_template("考试管理页面.html")


@app.route("/testPage/<int:page_id>/", methods=['GET', 'POST'])
def testPage(page_id):
    return render_template("考试答题页面.html")


@app.route("/testQuery", methods=['GET', 'POST'])
def testQuery():
    student = Student.query.get(session["uid"])
    pages = student.get_pages()
    return render_template("考试查询页面.html", pages=pages)


@app.route("/teacherSignUp", methods=['GET', 'POST'])
def teacherSignUp():
    form = RegisterFormTeacher()
    return render_template("教师注册页面.html", form=form)


# ===========================浩教师信息页面======================================
# ===========================教师信息页面======================================
@app.route("/teacherInfo", methods=['GET', 'POST'])
def teacherInfo():
    # =======================存储信息======================================
    if request.method == 'POST':
        teacher = Teacher.query.get(session["uid"])
        form = TeacherInfoForm(request.form)

        if teacher.checkPassword(form.pre_password.data):
            if form.new_password.data == form.ensure_password.data:
                teacher.name = form.name.data
                teacher.setPassword(form.new_password.data)
                db.session.commit()
                return redirect("logout")
            else:
                flash('新密码和确认密码不一致')
                return render_template("教师信息页面_B.html", form=form)

        else:
            flash("原密码错误！")
            return render_template("教师信息页面_B.html", form=form)

    else:
        form = TeacherInfoForm()
        teacher = Teacher.query.get(session["uid"])
        form.id.data = teacher.id
        form.name.data = teacher.name
        return render_template("教师信息页面_B.html", form=form)


@app.route("/studentInfo", methods=['GET', 'POST'])
def studentInfo():
    form = StudentInfoForm()
    user = Student.query.get(session["uid"])
    if request.method == "GET":
        form.id.data = user.id
        form.name.data = user.name
        # 年级列表
        localtime = time.localtime(time.time())
        if localtime.tm_mon >= 9:
            first_grade = localtime.tm_year
        else:
            first_grade = localtime.tm_year - 1
        a = first_grade - user.grade
        grades = [user.grade + a, user.grade - 1 + a, user.grade - 2 + a, user.grade - 3 + a]
        del grades[a]
        form.grade.choices = [(user.grade, user.grade),
                              (grades[0], grades[0]),
                              (grades[1], grades[1]),
                              (grades[2], grades[2])]

        college = College.query.get(user.college_id)
        form.college.choices = [(college.id, college.name)]
        major = Major.query.get(user.major_id)
        form.major.choices = [(major.id, major.name)]
        classes = Class.query.get(user.class_id)
        form.classes.choices = [(classes.id, classes.name)]
        return render_template("学生信息页面.html", form=form)
    else:
        name = form.name.data
        college_id = form.college.data
        grade = form.grade.data
        class_id = form.classes.data
        major_id = form.major.data
        new_password = form.new_password.data
        pre_password = form.pre_password.data

        college = College.query.get(college_id)
        form.college.choices = [(college_id, college.name)]
        major = Major.query.get(major_id)
        form.major.choices = [(major_id, major.name)]
        classes = Class.query.get(class_id)
        form.classes.choices = [(class_id, classes.name)]
        form.grade.choices = [(grade, grade)]

        if user.checkPassword(pre_password):
            if form.new_password.data == form.ensure_password.data:
                # 改资料
                try:
                    user.name = name
                    user.college_id = college_id
                    user.grade = grade
                    user.class_id = class_id
                    user.major_id = major_id
                    db.session.commit()
                except InternalError:
                    db.session.rollback()
                    flash("信息不完善，请重新输入！")
                    return render_template('学生信息页面.html', form=form)
                # 不为空，改新密码
                if new_password:
                    user.password = new_password
                    db.session.commit()
                    flash("修改成功！")
                    return redirect('/logout')
                # 为空
                else:
                    pass
                flash("修改成功！")
                return redirect('studentInfo')
            else:
                flash("两次密码不一致！")
                return render_template('学生信息页面.html', form=form)
        else:
            flash("密码错误！")
            return render_template('学生信息页面.html', form=form)


@app.route("/testCheck/<int:page_id>", methods=['GET', 'POST'])
def testCheck(page_id):
    page = Page.query.get(page_id)
    code = page.code

    my_answers = json.loads(page.answer)
    test_id_list = json.loads(page.content)
    contents = {"choice_question": [], "fill_blank_question": [], "true_false_question": [],
                "free_response_question": []}
    for key in contents.keys():
        for test_id in test_id_list[key]:
            test = Test.query.get(test_id)
            contents[key].append({"id": test.id, "question": test.question, "answer": test.answer,
                                  "my_answer": my_answers[str(test.id)],
                                  "flag": "right" if test.answer != my_answers[str(test.id)] else "wrong"})
    return render_template("试卷复查页面.html", code=code, contents=contents)


@app.route("/testCreater", methods=['GET', 'POST'])
def testCreater():
    if request.method == 'GET':
        form = TestCreaterForm()
        # 创建可选择科目数组
        choices = []
        subjects = Subject.query.all()
        for subject in subjects:
            choices.append((subject.id, subject.name))
        form.subject.choices = choices
        # 创建可选择班级数组
        choices = []
        classes = Class.query.all()
        for class_ in classes:
            choices.append((class_.id, class_.name))
        form.class_.choices = choices
        return render_template("教师创建考试页面_B.html", form=form)
    else:
        form = TestCreaterForm(request.form)
        page_structure = {}
        page_structure["choice_question"] = form.choice_question_number.data
        page_structure["fill_blank_question"] = form.fill_blank_question_number.data
        page_structure["true_false_question"] = form.true_false_question_number.data
        page_structure["free_response_question"] = form.free_response_question_number.data

        subject_id = form.subject.data
        classes = form.class_.data
        for class_id in classes:
            students = Class.query.get(int(class_id))
            for student in students:
                student_subject = StudentSubject(student_id=student.id, subject_id=subject_id)
                try:
                    db.session.add(student_subject)
                    db.session.commit()
                except IntegrityError:
                    db.session.rollback()
                    student_subject = StudentSubject.query.filter_by(student_id=session["uid"],
                                                                     subject_id=subject_id).first()
                teacher_s_s = TeacherSS(student_subject_id=student_subject.id, teacher_id=session["uid"])
                try:
                    db.session.add(teacher_s_s)
                    db.session.commit()
                except IntegrityError:
                    db.session.rollback()
                    teacher_s_s = TeacherSS.query.filter_by(student_subject_id=student_subject.id,
                                                            teacher_id=session["uid"]).first()
                page = Page()
                page.date = form.date.data
                page.time_start = form.start_time.data
                minute_num = form.time_length.data
                page.time_length = minute_num * 60
                page.level = form.level.data
                page.structure = json.dumps(page_structure)
                teacher_s_s.pages.append(page)
                db.session.commit()
        flash("考试计划创建成功")
        return redirect("/testList")


# ===============================================浩，教师列表页面（（（（（（（（（（（（=====================================
@app.route("/testList/", methods=['GET', 'POST'])
def testList():
    if request.method == 'GET':
        pages = Page.query.all()

        return render_template('考试列表页面_B.html', pages=pages)
    else:
        return redirect("/teacherMenu")


@app.route("/delete/", methods=['GET', 'POST'])
def delete():
    if request.method == 'GET':
        page = Page.query.get(request.args['id'])
        try:
            db.session.delete(page)
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            flash("已经开始的考试不可随意删除")
        return redirect('/testList/')


@app.route("/logout", methods=['GET', 'POST'])
def logout():
    session.clear()
    return redirect("index")


# 浩：教师注册页面==================================================================================
@app.route("/teacherRegister", methods=['GET', 'POST'])
def teacherRegister():
    if request.method == 'GET':
        form = RegisterFormTeacher()
        return render_template('教师注册页面.html', form=form)
    else:
        form = RegisterFormTeacher(request.form)
        if form.validate_on_submit():
            user = Teacher()
            user.id = form.id.data
            user.name = form.name.data
            user.setPassword(form.password.data)
            if Teacher.query.get(user.id) is not None:
                flash("此工号已经被注册！！！！")
                return render_template('教师注册页面.html', form=form)
            db.session.add(user)
            db.session.commit()

            return redirect('index')
        else:
            flash("输入有误，请重新输入")
            return render_template('教师注册页面.html', form=form)


@app.route("/studentRegister", methods=['GET', 'POST'])
def studentRegister():
    if request.method == "POST":
        form = RegisterFormStudent(request.form)
        id_ = int(request.form.get("id"))
        name = request.form.get("name")
        grade = request.form.get("grade")
        classes_id = request.form.get("classes")
        password = request.form.get("password")
        ensure_password = request.form.get("ensure_password")
        user = Student(id=id_, name=name, grade=grade, class_id=classes_id,
                       password=password)

        if password == ensure_password:
            try:
                db.session.add(user)
                db.session.commit()
                flash("注册成功！")
                pass
            except InternalError:
                db.session.rollback()
                flash("信息不完善，请重新输入！")
                return render_template('学生注册页面.html', form=form)
            except IntegrityError:
                db.session.rollback()
                flash("该学号已被其他用户注册，请联系管理员！")
                pass
            return redirect("/login")
            pass
        else:
            flash("两次密码不一致！")
            return redirect("/studentRegister")
            pass
    else:
        form = RegisterFormStudent()
        form.college.choices = [(1, '==wadada===')]
        form.major.choices = [(1, '请先选择学院')]
        localtime = time.localtime(time.time())
        if localtime.tm_mon >= 9:
            first_grade = localtime.tm_year
        else:
            first_grade = localtime.tm_year - 1
        form.grade.choices = [(first_grade - 3, first_grade - 3),
                              (first_grade - 2, first_grade - 2),
                              (first_grade - 1, first_grade - 1),
                              (first_grade, first_grade)]
        form.classes.choices = [(1, '请先选择专业')]
        return render_template("学生注册页面.html", form=form)


@app.route("/teacherInfoUpdate", methods=['GET', 'POST'])
def teacherInfoUpdate():
    return redirect("teacherInfo")


@app.route("/studentRegister/selects", methods=["POST"])
def studentRegisterSelects():
    print(request.form)
    data = {"data": []}
    if request.form['my_select'] == 'college':
        colleges = College.query.all()
        for college in colleges:
            data["data"].append({"id": college.id, "name": college.name})
        pass
    elif request.form['my_select'] == 'major':
        parent_id = request.form['parent_id']
        college = College.query.get(parent_id)
        for major in college.majors:
            data["data"].append({"id": major.id, "name": major.name})
        pass
    else:
        parent_id = request.form['parent_id']
        major = Major.query.get(parent_id)
        for class_ in major.classes:
            data["data"].append({"id": class_.id, "name": class_.name})
        pass
    return json.dumps(data)


@app.route("/createPage/<int:page_id>", methods=['GET', 'POST'])
def createPage(page_id):
    student = Student.query.get(session["uid"])
    if student.get_current_page() is None:
        page = Page.query.get(page_id)
        for tested_student in page.tested_students:
            if student.id == tested_student.id:
                flash("你已经参加过这场考试了")
                return redirect("/studentMenu")
        page.tested_students.append(student)
        if datetime.datetime.now().date() > page.date:
            flash("这场考试已经结束了")
            return redirect("/studentMenu")
        if (datetime.datetime.now() + datetime.timedelta(minutes=10)).date() <= page.date and (
                datetime.datetime.now() + datetime.timedelta(minutes=10)).time() <= page.time_start:
            flash("这场考试还没开始")
            return redirect("/studentMenu")
        page_structure_detail = {"choice_question": [0, 0, 0], "fill_blank_question": [0, 0, 0],
                                 "true_false_question": [0, 0, 0], "free_response_question": [0, 0, 0]}
        page_structure = json.loads(page.structure)
        test_list = {"choice_question": [], "fill_blank_question": [], "true_false_question": [],
                     "free_response_question": []}
        for key in page_structure_detail.keys():
            if page.level == 1:
                page_structure_detail[key][1] = int(page_structure[key] * 0.3)
                page_structure_detail[key][2] = int(page_structure[key] * 0.1)
                page_structure_detail[key][0] = int(
                    page_structure[key] - page_structure_detail[key][1] - page_structure_detail[key][2])
            if page.level == 2:
                page_structure_detail[key][1] = int(page_structure[key] * 0.6)
                page_structure_detail[key][2] = int(page_structure[key] * 0.2)
                page_structure_detail[key][0] = int(
                    page_structure[key] - page_structure_detail[key][1] - page_structure_detail[key][2])
            if page.level == 3:
                page_structure_detail[key][1] = int(page_structure[key] * 0.4)
                page_structure_detail[key][2] = int(page_structure[key] * 0.4)
                page_structure_detail[key][0] = int(
                    page_structure[key] - page_structure_detail[key][1] - page_structure_detail[key][2])
        for key in test_list.keys():
            for i in range(3):
                test_list_list = Test.query.filter(Test.id_subject == page.id_subject).filter(
                    Test.type_ == key).filter(Test.level == i + 1).order_by(func.rand()).limit(
                    page_structure_detail[key][i])
                for test in test_list_list:
                    test_list[key].append(test)

        id_list = {"choice_question": [], "fill_blank_question": [], "true_false_question": [],
                   "free_response_question": []}
        for key in id_list.keys():
            for test in test_list[key]:
                id_list[key].append(test.id)

        page = Page.query.get(page_id)
        page.content = json.dumps(id_list)
        page.rest_time = page.time_length * 60
        page.ongoing = True
        db.session.commit()
    else:
        page = student.get_current_page()
        id_list = json.loads(page.content)
        pass

    contents = {"choice_question": [], "fill_blank_question": [], "true_false_question": [],
                "free_response_question": []}
    test_num = 0
    for type_ in id_list:
        for id_ in id_list[type_]:
            test = Test.query.get(id_)
            contents[type_].append({"id": test.id, "question": test.question})
            test_num += 1
    rest_seconds = page.rest_time

    test_num = 0
    ps = page.tb_plan.page_structure
    ps = json.loads(ps)
    for key in ps.keys():
        test_num += int(ps[key])

    return render_template('考试页面.html', contents=contents, rest_time=rest_seconds,
                           answer=json.loads(page.answer) if page.answer else "", test_num=test_num)


@app.route("/get_score", methods=['GET', 'POST'])
def get_score():
    right_num = 0
    answer = {}

    if len(request.form) != 0:
        for key in request.form:
            test = Test.query.get(key)
            answer[key] = request.form[key]
            if test.answer == request.form[key]:
                right_num += 1
            else:
                pass
        score = 100 * right_num / len(request.form)
    else:
        score = 0

    student = Student.query.get(session["uid"])
    page = student.get_current_page()
    page.ongoing = False
    page.code = score
    page.answer = json.dumps(answer)
    db.session.add(page)
    db.session.commit()
    # return "<h1>分数：%d</h1><br>" % score
    return redirect(url_for("testCheck", page_id=temp_page_id))


@app.route("/auto_save", methods=['GET', 'POST'])
def auto_save():
    answer ={}
    rest_time = 0
    if len(request.form) != 0:
        for key in request.form:
            if key == "rest_time":
                rest_time = int(request.form[key])
            else:
                answer[key] = request.form[key]
        student = Student.query.get(session["uid"])
        page = student.get_current_page()
        page.rest_time = rest_time
        page.answer = json.dumps(answer)
        db.session.commit()
    else:
        pass
    return str(rest_time)

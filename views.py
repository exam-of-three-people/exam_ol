from flask import render_template, redirect, flash, url_for, request, json, session
from forms import LoginForm, RegisterFormStudent, RegisterFormTeacher, StudentInfoForm, TeacherInfoForm, TestCreaterForm
from models import app, Student, Teacher, College, Major, Subject, Plan, Page, Test, Class, TestType, classes_plans, db
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
    id_class = student.id_class
    class_ = Class.query.get(id_class)
    now = datetime.datetime.now()
    plans = Plan.query.filter(Plan.date >= now.date()).with_parent(class_).all()
    return render_template("学生菜单_B.html", plans=plans)


@app.route("/teacherMenu", methods=['GET', 'POST'])
def teacherMenu():
    return render_template("教师菜单_B.html")


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
    tests = [{"第一次考试": 1}, {"第二次考试": 2}]
    return render_template("考试查询页面.html", tests=tests)


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

        college = College.query.get(user.id_college)
        form.college.choices = [(college.id, college.name)]
        major = Major.query.get(user.id_major)
        form.major.choices = [(major.id, major.name)]
        classes = Class.query.get(user.id_class)
        form.classes.choices = [(classes.id, classes.name)]
        return render_template("学生信息页面_B.html", form=form)
    else:
        name = form.name.data
        id_college = form.college.data
        grade = form.grade.data
        id_class = form.classes.data
        id_major = form.major.data
        new_password = form.new_password.data
        pre_password = form.pre_password.data

        college = College.query.get(id_college)
        form.college.choices = [(id_college, college.name)]
        major = Major.query.get(id_major)
        form.major.choices = [(id_major, major.name)]
        classes = Class.query.get(id_class)
        form.classes.choices = [(id_class, classes.name)]
        form.grade.choices = [(grade, grade)]

        if user.checkPassword(pre_password):
            if form.new_password.data == form.ensure_password.data:
                # 改资料
                try:
                    user.name = name
                    user.id_college = id_college
                    user.grade = grade
                    user.id_class = id_class
                    user.id_major = id_major
                    db.session.commit()
                except InternalError:
                    db.session.rollback()
                    flash("信息不完善，请重新输入！")
                    return render_template('学生信息页面_B.html', form=form)
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
                return render_template('学生信息页面_B.html', form=form)
        else:
            flash("密码错误！")
            return render_template('学生信息页面_B.html', form=form)


@app.route("/testCheck/<int:page_id>", methods=['GET', 'POST'])
def testCheck(page_id):
    return render_template("试卷复查页面.html")


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
        pageStructure = {}
        pageStructure["choice_question"] = form.choice_question_number.data
        pageStructure["fill_blank_question"] = form.fill_blank_question_number.data
        pageStructure["true_false_question"] = form.true_false_question_number.data
        pageStructure["free_response_question"] = form.free_response_question_number.data

        plan = Plan()
        plan.id_subject = form.subject.data
        plan.date = form.date.data
        plan.time_start = form.start_time.data
        minute_num = form.time_length.data
        plan.time_length = datetime.timedelta(minutes=minute_num)
        plan.level = form.level.data
        plan.page_structure = json.dumps(pageStructure)

        classes = form.class_.data
        for class_id in classes:
            plan.classes.append(Class.query.get(class_id))
        db.session.add(plan)
        db.session.commit()
        return redirect("/teacherMenu")


# ===============================================浩，教师列表页面（（（（（（（（（（（（=====================================
@app.route("/testList/", methods=['GET', 'POST'])
def testList():
    if request.method == 'GET':
        plans = Plan.query.all()

        return render_template('考试列表页面_B.html', plans=plans, Subject=Subject)
    else:
        return render_template('教师菜单.html')


@app.route("/delete/", methods=['GET', 'POST'])
def delete():
    if request.method == 'GET':
        plan = Plan.query.get(request.args['id'])
        try:
            db.session.delete(plan)
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
        id = int(request.form.get("id"))
        name = request.form.get("name")
        college_id = request.form.get("college")
        grade = request.form.get("grade")
        classes_id = request.form.get("classes")
        major_id = request.form.get("major")
        password = request.form.get("password")
        ensure_password = request.form.get("ensure_password")
        user = Student(id=id, name=name, id_college=college_id, id_major=major_id, grade=grade, id_class=classes_id,
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
        for clas in major.classes:
            data["data"].append({"id": clas.id, "name": clas.name})
        pass
    return json.dumps(data)


@app.route("/createPage/<int:id_plan>", methods=['GET', 'POST'])
def createPage(id_plan):
    student = Student.query.get(session["uid"])
    if student.current_page_id is None:
        plan = Plan.query.get(id_plan)
        for tested_student in plan.tested_students:
            if student.id == tested_student.id:
                flash("你已经参加过这场考试了")
                return redirect("/studentMenu")
        plan.tested_students.append(student)
        if datetime.datetime.now().date() > plan.date:
            flash("这场考试已经结束了")
            return redirect("/studentMenu")
        if (datetime.datetime.now()+datetime.timedelta(minutes=10)).date() <= plan.date and (datetime.datetime.now()+datetime.timedelta(minutes=10)).time() <= plan.time_start:
            flash("这场考试还没开始")
            return redirect("/studentMenu")
        page_structure_detail = {"choice_question": [0, 0, 0], "fill_blank_question": [0, 0, 0],
                                 "true_false_question": [0, 0, 0], "free_response_question": [0, 0, 0]}
        page_structure = json.loads(plan.page_structure)
        test_list = {"choice_question": [], "fill_blank_question": [], "true_false_question": [],
                     "free_response_question": []}
        for key in page_structure_detail.keys():
            if plan.level == 1:
                page_structure_detail[key][1] = int(page_structure[key] * 0.3)
                page_structure_detail[key][2] = int(page_structure[key] * 0.1)
                page_structure_detail[key][0] = int(
                    page_structure[key] - page_structure_detail[key][1] - page_structure_detail[key][2])
            if plan.level == 2:
                page_structure_detail[key][1] = int(page_structure[key] * 0.6)
                page_structure_detail[key][2] = int(page_structure[key] * 0.2)
                page_structure_detail[key][0] = int(
                    page_structure[key] - page_structure_detail[key][1] - page_structure_detail[key][2])
            if plan.level == 3:
                page_structure_detail[key][1] = int(page_structure[key] * 0.4)
                page_structure_detail[key][2] = int(page_structure[key] * 0.4)
                page_structure_detail[key][0] = int(
                    page_structure[key] - page_structure_detail[key][1] - page_structure_detail[key][2])
        for key in test_list.keys():
            test_type = TestType.query.filter(TestType.name == key).first()
            for i in range(3):
                test_list_list = Test.query.filter(Test.id_subject == plan.id_subject).filter(
                    Test.type == test_type.id).filter(Test.level == i + 1).order_by(func.rand()).limit(
                    page_structure_detail[key][i])
                for test in test_list_list:
                    test_list[key].append(test)

        id_list = {"choice_question": [], "fill_blank_question": [], "true_false_question": [],
                   "free_response_question": []}
        for key in id_list.keys():
            for test in test_list[key]:
                id_list[key].append(test.id)

        page = Page()
        page.content = json.dumps(id_list)
        page.id_plan = id_plan
        page.id_student = session["uid"]
        page.rest_time = plan.time_length
        db.session.add(page)
        db.session.commit()

        student.current_page_id = page.id
        db.session.commit()

    else:
        page = Page.query.get(student.current_page_id)
        id_list = json.loads(page.content)
        pass

    contents = {"choice_question": [], "fill_blank_question": [], "true_false_question": [],
                "free_response_question": []}
    for type_ in id_list:
        for id_ in id_list[type_]:
            test = Test.query.get(id_)
            contents[type_].append({"id": test.id, "question": test.question,
                                    "answer": json.loads(page.answer)[id_] if page.answer else ""})

    return render_template('考试页面.html', contents=contents, rest_time=page.rest_time)


@app.route("/get_score", methods=['GET', 'POST'])
def get_score():
    right_num = 0
    answer = []

    if len(request.form) != 0:
        for key in request.form:
            test = Test.query.get(key)
            answer.append({key: request.form[key]})
            if test.answer == request.form[key]:
                right_num += 1
            else:
                pass
        score = 100 * right_num / len(request.form)
    else:
        score = 0

    student = Student.query.get(session["uid"])
    page = Page.query.get(student.current_page_id)
    student.current_page_id = None
    page.code = score
    page.answer = json.dumps(answer)
    db.session.add(page)
    db.session.commit()
    return "<h1>分数：%d</h1><br>" % score


@app.route("/auto_save", methods=['GET', 'POST'])
def auto_save():
    answer ={}
    if len(request.form) != 0:
        for key in request.form:
            if key == "rest_time":
                rest_time = int(request.form[key])
            else:
                answer[key] = request.form[key]
        student = Student.query.filter(Student.id == session["uid"])
        page = Page.query.get(student.current_page_id)
        page.rest_time = datetime.timedelta(seconds= rest_time)
        page.answer = answer
        db.session.commit()
    else:
        pass
    return rest_time

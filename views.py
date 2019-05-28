import datetime
import json
import time

from flask import render_template, redirect, flash, url_for, request, json, session
from sqlalchemy import func
from sqlalchemy.exc import IntegrityError, InternalError

from forms import LoginForm, RegisterFormStudent, RegisterFormTeacher, StudentInfoForm, TeacherInfoForm, TestCreaterForm
from models import app, Student, Teacher, College, Major, StudentSubject, TeacherSS, Subject, Page, Test, Class, db


@app.route("/", methods=['GET', 'POST'])
@app.route("/index", methods=['GET', 'POST'])
@app.route("/login", methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        form = LoginForm(request.form)
        if form.validate_on_submit():
            id_ = int(form.id.data)
            password = form.password.data
            if form.role.data == 1:
                user = Student.query.get(id_)
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
                user = Teacher.query.get(id_)
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
    return render_template("登录页面.html", form=form)


@app.route("/studentMenu", methods=['GET', 'POST'])
def studentMenu():
    student = Student.query.get(session["uid"])
    now = datetime.datetime.now()
    pages = student.get_pages()
    pages_show = []
    for page in pages:
        # 已经参加过的考试不再显示
        # if not page.finshed and page.date == now.date():
        #     pages_show.append(page)
        pages_show.append(page)
    return render_template("学生菜单.html", pages=pages_show)


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
                return render_template("教师信息页面.html", form=form)

        else:
            flash("原密码错误！")
            return render_template("教师信息页面.html", form=form)

    else:
        form = TeacherInfoForm()
        teacher = Teacher.query.get(session["uid"])
        form.id.data = teacher.id
        form.name.data = teacher.name
        return render_template("教师信息页面.html", form=form)


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
        a = first_grade - user.class_.grade
        grades = [user.class_.grade + a, user.class_.grade - 1 + a, user.class_.grade - 2 + a,
                  user.class_.grade - 3 + a]
        del grades[a]
        form.grade.choices = [(user.class_.grade, user.class_.grade),
                              (grades[0], grades[0]),
                              (grades[1], grades[1]),
                              (grades[2], grades[2])]

        college = user.class_.major.college
        form.college.choices = [(college.id, college.name)]
        major = user.class_.major
        form.major.choices = [(major.id, major.name)]
        class_ = user.class_
        form.class_.choices = [(class_.id, class_.name)]
        return render_template("学生信息页面.html", form=form)
    else:
        name = form.name.data
        college_id = form.college.data
        grade = form.grade.data
        class_id = form.class_.data
        major_id = form.major.data
        new_password = form.new_password.data
        pre_password = form.pre_password.data

        college = College.query.get(college_id)
        form.college.choices = [(college_id, college.name)]
        major = Major.query.get(major_id)
        form.major.choices = [(major_id, major.name)]
        class_ = Class.query.get(class_id)
        form.class_.choices = [(class_id, class_.name)]
        form.grade.choices = [(grade, grade)]

        if user.checkPassword(pre_password):
            if form.new_password.data == form.ensure_password.data:
                # 改资料
                try:
                    user.name = name
                    user.college_id = college_id
                    user.class_.grade = grade
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
    contents = {"选择题": [], "填空题": [], "判断题": [], "解答题": []}
    for key in contents.keys():
        for test_id in test_id_list[key]:
            test = Test.query.get(test_id)
            contents[key].append({"id": test.id, "question": test.question, "answer": test.answer,
                                  "my_answer": my_answers[str(test.id)],
                                  "flag": "right" if test.answer == my_answers[str(test.id)] else "wrong"})
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
        return render_template("教师创建考试页面.html", form=form)
    else:
        flash("创建时间可能较长,请耐心等待....")
        form = TestCreaterForm(request.form)
        page_structure = {}
        page_structure["选择题"] = form.choice_question_number.data
        page_structure["填空题"] = form.fill_blank_question_number.data
        page_structure["判断题"] = form.true_false_question_number.data
        page_structure["解答题"] = form.free_response_question_number.data

        subject_id = form.subject.data
        classes = form.class_.data
        for class_id in classes:
            class_ = Class.query.get(int(class_id))
            students = class_.students
            for student in students:
                student_subject = StudentSubject.query.filter_by(student_id=student.id,
                                                                 subject_id=subject_id).first()
                if student_subject is None:
                    student_subject = StudentSubject(student_id=student.id, subject_id=subject_id)
                    db.session.add(student_subject)
                    db.session.commit()
                teacher_s_s = TeacherSS.query.filter_by(student_subject_id=student_subject.id,
                                                        teacher_id=session["uid"]).first()
                if teacher_s_s is None:
                    teacher_s_s = TeacherSS(student_subject_id=student_subject.id, teacher_id=session["uid"])
                    db.session.add(teacher_s_s)
                    # db.session.commit()
                page = Page()
                page.name = form.name.data
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
        teacher = Teacher.query.get(session["uid"])
        pages = teacher.get_pages()
        pages_show = []
        is_repeat = False
        for page in pages:
            for page_show in pages_show:
                if page.date == page_show["page"].date and page.time_start == page_show["page"].time_start \
                        and page.teacher_s_s.student_subject.subject.id == page_show[
                    "page"].teacher_s_s.student_subject.id:
                    is_repeat = True
                    if page.teacher_s_s.student_subject.student.class_id not in page_show["classes"]:
                        page_show["classes"].append(page.teacher_s_s.student_subject.student.class_id)
                    break
                is_repeat = False
            if not is_repeat:
                pages_show.append({"page": page, "classes": []})
        return render_template('考试列表页面.html', pages=pages_show, Class=Class)
    else:
        return redirect("/teacherMenu")


@app.route("/delete/", methods=['GET', 'POST'])
def delete():
    if request.method == 'GET':
        teacher = Teacher.query.get(session["uid"])
        page_delete = Page.query.get(request.args['id'])
        pages = teacher.get_pages()
        pages_delete = []
        for page in pages:
            if page.date == page_delete.date \
                    and page.time_start == page_delete.time_start:
                pages_delete.append(page)

        try:
            for page_delete in pages_delete:
                db.session.delete(page_delete)
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
            if class_.grade == int(request.form['grade']):
                data["data"].append({"id": class_.id, "name": class_.name})
        pass
    return json.dumps(data)


@app.route("/createPage/<int:page_id>", methods=['GET', 'POST'])
def createPage(page_id):
    student = Student.query.get(session["uid"])
    if student.get_current_page() is None:
        page = Page.query.get(page_id)
        # for tested_student in page.tested_students:
        #     if student.id == tested_student.id:
        #         flash("你已经参加过这场考试了")
        #         return redirect("/studentMenu")
        # page.tested_students.append(student)
        # if datetime.datetime.now().date() > page.date:
        #     flash("这场考试已经结束了")
        #     return redirect("/studentMenu")
        # if (datetime.datetime.now() + datetime.timedelta(minutes=10)).date() <= page.date and (
        #         datetime.datetime.now() + datetime.timedelta(minutes=10)).time() <= page.time_start:
        #     flash("这场考试还没开始")
        #     return redirect("/studentMenu")
        page_structure_detail = {"选择题": [0, 0, 0], "填空题": [0, 0, 0],
                                 "判断题": [0, 0, 0], "解答题": [0, 0, 0]}
        page_structure = json.loads(page.structure)
        test_list = {"选择题": [], "填空题": [], "判断题": [],
                     "解答题": []}
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
                test_list_list = Test.query.filter(
                    Test.subject_id == page.teacher_s_s.student_subject.subject.id).filter(
                    Test.type_ == key).filter(Test.level == i + 1).order_by(func.rand()).limit(
                    page_structure_detail[key][i])
                for test in test_list_list:
                    test_list[key].append(test)

        id_list = {"选择题": [], "填空题": [], "判断题": [], "解答题": []}
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

    contents = {"选择题": [], "填空题": [], "判断题": [], "解答题": []}
    test_num = 0
    for type_ in id_list:
        for id_ in id_list[type_]:
            test = Test.query.get(id_)
            contents[type_].append({"id": test.id, "question": test.question})
            test_num += 1
    rest_seconds = page.rest_time

    return render_template('考试页面.html', contents=contents, rest_time=rest_seconds,
                           answer=json.loads(page.answer) if page.answer else "", test_num=test_num)


@app.route("/get_score", methods=['GET', 'POST'])
def get_score():
    right_num = 0
    answer = {}
    scores = {}

    if len(request.form) != 0:
        for key in request.form:
            test = Test.query.get(key)
            answer[key] = request.form[key]
            if test.answer == request.form[key]:
                scores[key] = 100 / len(request.form)
                right_num += 1
            else:
                pass
        score = 100 * right_num / len(request.form)
    else:
        score = 0

    student = Student.query.get(session["uid"])
    page = student.get_current_page()
    page.scores = json.dumps(scores)
    page.ongoing = False
    page.code = score
    page.answer = json.dumps(answer)
    db.session.add(page)
    db.session.commit()
    # return "<h1>分数：%d</h1><br>" % score
    return redirect(url_for("testCheck", page_id=page.id))


@app.route("/auto_save", methods=['GET', 'POST'])
def auto_save():
    answer = {}
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


@app.route("/analyse", methods=['GET', 'POST'])
def analyse():
    date = datetime.datetime.strptime(request.args['date'], "%Y-%m-%d")
    time_start = datetime.datetime.strptime(request.args["time_start"], "%H:%M:%S")
    subject_id = request.args["subject_id"]
    current_class_id = request.args["current_class_id"]
    current_button = request.args["current_button"]

    first_flag = True

    pages_classes_query = Page.query.filter(Page.teacher_s_s.teacher.id == session["uid"],
                                            Page.date == date,
                                            Page.time_start == time_start,
                                            Page.teacher_s_s.student_subject.subject.id == subject_id)

    # 所有相关班级
    classes_id = []
    for page in pages_classes_query.all():
        class_id = page.teacher_s_s.student_subject.student.class_id
        if class_id not in classes_id:
            classes_id.append(class_id)
    # 试卷涉及的所有班级
    classes = []
    for class_id in classes_id:
        class_ = Class.query.get(class_id)
        classes.append(class_)

    # 当前选中班级
    if current_class_id != 0:
        pages_one_class_query = pages_classes_query.filter(
            Page.teacher_s_s.student_subject.student.class_id == current_class_id)
    else:
        pages_one_class_query = pages_classes_query

    if current_button == "统计数据":
        # 数据结构准备
        data = {"各小题": {"选择题": [], "填空题": [], "判断题": [], "解答题": []},
                "各题型": {"选择题": {"平均分": 0, "最高分": 0, "最低分": 1000},
                        "填空题": {"平均分": 0, "最高分": 0, "最低分": 1000},
                        "判断题": {"平均分": 0, "最高分": 0, "最低分": 1000},
                        "解答题": {"平均分": 0, "最高分": 0, "最低分": 1000}},
                "各分数段": {"0~59": 0, "60~69": 0, "70~79": 0, "80~89": 0, "90~100": 0},
                "总分": {"平均分": 0, "及格率": 0, "最高分": 0, "最低分": 0, "优秀率": 0},
                "及格人数": 0,
                "应考人数": 0,
                "实考人数": 0}
        test_number = 0
        page_number = 0
        finished_number = 0
        should_number = 0

        for page in pages_one_class_query.all():
            should_number += 1
            # 生成各小题得分率数据结构
            if first_flag:
                contents = json.loads(page.content)
                for key in contents.keys():
                    data["各小题"][key] = []
                    for test in contents[key]:
                        data["各小题"][key].append({"题目ID": test["id"], "得分率": 0})
                        test_number += 1

            # 计算各小题得分总数
            scores = json.loads(page.scores)
            if page.finished:
                finished_number += 1
                for test_type in data["各小题"].keys():
                    this_type_score = 0
                    for i in range(len(data["各小题"][test_type])):
                        test_id = data["各小题"][test_type][i]["题目ID"]
                        data["各小题"][test_type][i]["得分率"] += scores[test_id]
                        this_type_score += scores[test_id]
                    # 各题型总分数
                    data["各题型"][test_type]["平均分"] += this_type_score
                    if data["各题型"][test_type]["最高分"] < this_type_score:
                        data["各题型"][test_type]["最高分"] = this_type_score
                    if data["各题型"][test_type]["最低分"] > this_type_score:
                        data["各题型"][test_type]["最低分"] = this_type_score
                # 试卷总分
                data["总分"]["平均分"] += page.code
                if data["总分"]["最高分"] < page.code:
                    data["总分"]["最高分"] = page.code
                if data["总分"]["最低分"] > page.code:
                    data["总分"]["最低分"] = page.code

                if 0 <= page.code <= 59:
                    data["各分数段"]["0~59"] += 1
                elif 60 <= page.code <= 69:
                    data["各分数段"]["60~69"] += 1
                elif 70 <= page.code <= 79:
                    data["各分数段"]["80~89"] += 1
                elif 80 <= page.code <= 89:
                    data["各分数段"]["80~89"] += 1
                else:
                    data["各分数段"]["90~100"] += 1
            else:
                # 有些人就是不参加考试,我还要为他写个if语句
                for test_type in data["各小题"].keys():
                    data["各题型"][test_type]["最低分"] = 0
                data["各分数段"]["0~59"] += 1

            page_number += 1
            first_flag = False
        # 各种平均分
        for test_type in data["各小题"].keys():
            for i in range(len(data["各小题"][test_type])):
                data["各小题"][test_type][i]["得分率"] /= page_number * test_number
            data["各题型"][test_type]["平均分"] /= page_number
        data["总分"]["平均分"] /= page_number
        # 计算各分数段比例:
        for key in data["各分数段"].keys():
            data["各分数段"][key] /= page_number
        # 优秀与及格率:
        data["总分"]["优秀率"] = (data["各分数段"]["80~89"] + data["各分数段"]["90~100"]) / page_number
        data["总分"]["及格率"] = 1 - (data["各分数段"]["0~59"]) / page_number
        return render_template("统计数据页面.html", classes=classes, data=data, current_class_id=current_class_id,
                               current_button=current_button, date=date, time_start=time_start)
    else:
        # 初始化数据结构
        data = []
        data_item = {"学号": 0, "姓名": 0,
                     "选择题": {"总分": 0, "各小题": []},
                     "填空题": {"总分": 0, "各小题": []},
                     "判断题": {"总分": 0, "各小题": []},
                     "简答题": {"总分": 0, "各小题": []}}
        for page in pages_one_class_query.all():
            data_item["学号"] = page.teacher_s_s.student_subject.student.id
            data_item["姓名"] = page.teacher_s_s.student_subject.student.name
            scores = json.loads(page.scores)
            contents = json.loads(page.content)
            for key in contents.keys():
                this_type_score = 0
                for test in contents[key]:
                    score = scores[str(test["id"])]
                    data_item[key]["各小题"].append(score)
                    this_type_score += score
                data_item[key]["总分"] = this_type_score
            data.append(data_item)
        return render_template("原始数据页面.html", classes=classes, data=data, current_class_id=current_class_id,
                               current_button=current_button, date=date, time_start=time_start)

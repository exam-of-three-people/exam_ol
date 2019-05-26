# -*- coding: utf-8 -*-
# @Time    : 2019/5/19 下午5:41
# @Author  : xianfa
# @FileName: 删库不跑路.py
# @Software: PyCharm
from models import Test, db, TestType, College, Class, Subject, Student, Major, Teacher, Page, Plan


answer_random = ['A', 'B', 'C', 'D']
level_random = [1, 2, 3]
question_random = "qwertyuiopasdfghjklzxcvbnm"
type_names = ["choice_question", "fill_blank_question", "true_false_question", "free_response_question"]

subjects = []
colleges = []
majors = []
classes = []
for i in range(1,9):
    colleges.append("学院"+str(i))
    majors.append("专业"+str(i))
    classes.append("_"+str(i) + "班")
    subjects.append("学科"+str(i))

for college_name in colleges:
    college = College()
    college.name = college_name
    db.session.add(college)
db.session.commit()
print("学院创建完毕")

for i in range(1,9):
    for major_name in majors:
        major = Major()
        major.name = colleges[i-1] + major_name
        major.college_id = i
        db.session.add(major)
db.session.commit()
print("专业创建完毕")

for i in range(1,9):
    for j in range(1,9):
        for class_name in classes:
            class_ = Class()
            class_.name = colleges[i-1]+majors[j-1]+class_name
            class_.id_major = (i-1)*8+j
            db.session.add(class_)
db.session.commit()
print("班创建完毕")

for i in range(1,9):
    for j in range(1,9):
        for k in range(1,9):
            for l in range(1,9):
                for m in [2015,2016,2017,2018]:
                    id = m*10**6+i*10**5+j*10**4+k*10**3+l*10**2
                    student = Student()
                    student.id = id
                    student.name = "随机名" + str(i)+str(j)+str(k)+str(l)
                    student.id_college = i
                    student.id_major = (i-1)*8+j
                    student.class_id = ((i - 1) * 8 + j - 1) * 8 + k
                    student.grade = m
                    student.password_hash = "pbkdf2:sha256:150000$LssWNeqi$de05643547efe747ad0a14b74ac2e0e036e2d21fcae3be98bd43c94392f2226d"
                    db.session.add(student)
db.session.commit()
print("学生创建完毕")

for i in range(1,9):
    teacher = Teacher()
    teacher.id = i*100
    teacher.name = "随机名"+str(i)
    teacher.password_hash = "pbkdf2:sha256:150000$LssWNeqi$de05643547efe747ad0a14b74ac2e0e036e2d21fcae3be98bd43c94392f2226d"
    db.session.add(teacher)
db.session.commit()
print("教师创建完毕")

for subject_name in subjects:
    subject = Subject()
    subject.name= subject_name
    db.session.add(subject)
db.session.commit()
print("学科创建完毕")

# 删题
tests = Test.query.all()
for test in tests:
    db.session.remove(test)
db.session.commit()
# 删题型
types = TestType.query.all()
for type in types:
    db.session.remove(type)
db.session.commit()
# 建题型
for type_name in type_names:
    type = TestType()
    type.name=type_name
    db.session.add(type)
db.session.commit()
# 选择题
for answer in ['A', 'B', 'C', 'D']:
    for level in range(1, 3+1):
        for subject in subjects:
            for ch in question_random:
                question = "☆" * level + answer + "是这题的答案，" + ch + "是个随机字母。" + "题型是选择题"
                test = Test()
                test.type = 1
                test.question = question
                test.answer = answer
                test.id_subject = int(subject[-1])
                test.level = level
                db.session.add(test)
db.session.commit()
print("选择题创建完毕")
# 填空题
for answer in ['A', 'B', 'C', 'D']:
    for level in range(1, 3+1):
        for subject in subjects:
            for ch in question_random:
                question = "☆" * level + answer + "是这题的答案，" + ch + "是个随机字母。" + "题型是填空题"
                test = Test()
                test.type = 2
                test.question = question
                test.answer = answer
                test.id_subject = int(subject[-1])
                test.level = level
                db.session.add(test)
db.session.commit()
print("填空题创建完毕")
# 判断题
for answer in ['0', '1', '0', '1']:
    for level in range(1, 3+1):
        for subject in subjects:
            for ch in question_random:
                question = "☆" * level + answer + "是这题的答案，" + ch + "是个随机字母。" + "题型是判断题。"+ "0代表错误，1代表正确"
                test = Test()
                test.type = 3
                test.question = question
                test.answer = answer
                test.id_subject = int(subject[-1])
                test.level = level
                db.session.add(test)
db.session.commit()
print("判断题创建完毕")
# 解答题
for answer in ['A', 'B', 'C', 'D']:
    for level in range(1, 3+1):
        for subject in subjects:
            for ch in question_random:
                question = "☆" * level + answer + "是这题的答案，" + ch + "是个随机字母。" + "题型是解答题"
                test = Test()
                test.type = 4
                test.question = question
                test.answer = answer
                test.id_subject = int(subject[-1])
                test.level = level
                db.session.add(test)
db.session.commit()
print("解答题创建完毕")

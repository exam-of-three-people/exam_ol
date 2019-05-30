# -*- coding: utf-8 -*-
# @Time    : 2019/5/29 下午4:51
# @Author  : xianfa
# @FileName: 自动考试.py
# @Software: PyCharm
import json
import random

from sqlalchemy import func

from models import Page, Test, db

pages = Page.query.all()

random_bool = [True, True, False, True, True, False, True, True, ]

for page in pages:
    page_structure_detail = {"选择题": [0, 0, 0], "填空题": [0, 0, 0],
                             "判断题": [0, 0, 0], "解答题": [0, 0, 0]}
    page_structure = json.loads(page.structure)
    test_list = {"选择题": [], "填空题": [], "判断题": [],
                 "解答题": []}
    answer = {}

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
    scores = {"选择题": {}, "填空题": {}, "判断题": {}, "解答题": {}}
    test_num = 0
    right_num = 0
    for type_ in page_structure:
        test_num += page_structure[type_]
    for key in id_list.keys():
        for test in test_list[key]:
            id_list[key].append(test.id)
            if random.choice(random_bool):
                answer[str(test.id)] = test.answer
                right_num += 1
                scores[key][str(test.id)] = 100 // test_num
            else:
                answer[str(test.id)] = ''
                scores[key][str(test.id)] = 0

    page.content = json.dumps(id_list)
    page.answer = json.dumps(answer)
    page.scores = json.dumps(scores)
    page.rest_time = page.time_length * 60
    page.code = 100 * right_num // test_num
    page.ongoing = True
    page.finished = True
    db.session.commit()

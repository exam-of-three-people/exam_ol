# -*- coding: utf-8 -*-
# @Time    : 2019/5/19 下午5:41
# @Author  : xianfa
# @FileName: 题目生成器.py
# @Software: PyCharm
from models import Test, db

answer_random = ['A', 'B', 'C', 'D']
level_random = [1, 2, 3]
question_random = "qwertyuiopasdfghjklzxcvbnm"
type_names = ["choice_question", "fill_blank_question", "true_false_question", "free_response_question"]
subjects = [1]
types = [3,4,5,6]
for answer in answer_random:
    for level in level_random:
        for type in types:
            for subject in subjects:
                for ch in question_random:
                    question = "☆" * level + answer + "是这题的答案，" + ch + "是个随机字母。" + "题型" + type_names[type-3]
                    test = Test()
                    test.type = type
                    test.question = question
                    test.answer = answer
                    test.id_subject = subject
                    test.level = level
                    db.session.add(test)
                    db.session.commit()

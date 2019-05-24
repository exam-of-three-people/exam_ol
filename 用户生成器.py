import random



colleges = ['计算机科学与工程学院', '化工与制药学院', '电气信息学院', '土木工程与建筑学院', '材料科学与工程学院', '管理学院', '法商学院', '化学与环境工程学院', '光电信息与能源工程学院',
            '数理学院', '外语学院.', '艺术设计学院', '继续教育学院', '国际学院', '马克思主义学院', '环境生态与生物工程学院']

majors = {'计算机科学与工程学院': ['智能科学与技术']}

persons = []

i = 0
while (i <= 3000):
    sex = random.choice(['female', 'male'])
    name = random.choice(last_names) + random.choice(first_names[sex])
    college = random.choice(colleges)
    persons.append({'sex': sex, 'name': name, 'college': college})
    i += 1

for item in persons:
    print(item)

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config["SECRET_KEY"] = "123456"
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:qwer@localhost:3306/exam_ol_database"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
app.config["SQLALCHEMY_COMMIT_ON_TEARDOWN"] = True

db = SQLAlchemy(app)


class Student(db.Model):
    __tablename__ = "tb_student"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(10), nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    grade = db.Column(db.Integer, nullable=False)
    id_class = db.Column(db.Integer, db.ForeignKey('tb_class.id'), nullable=False)
    current_page_id = db.Column(db.Integer, nullable=True, default=None)

    pages = db.relationship("Page", backref="tb_student")

    @property
    def password(self):
        return AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def checkPassword(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return ("[学生 %r]" % self.id)

    pass


class Teacher(db.Model):
    __tablename__ = "tb_teacher"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(10), nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    # def insertTeacher(self,user):
    #     db.session.add(user)
    def checkPassword(self, password):
        return check_password_hash(self.password_hash, password)

    def setPassword(self, password):
        self.password_hash = generate_password_hash(password)

    def __repr__(self):
        return "[%r老师]" % self.name

    pass


class College(db.Model):
    __tablename__ = "tb_college"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(16), nullable=False)

    majors = db.relationship("Major", backref="tb_college")

    def __repr__(self):
        return "[学院 %r]" % self.name

    pass


class Major(db.Model):
    __tablename__ = "tb_major"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(16), nullable=False)
    id_college = db.Column(db.Integer, db.ForeignKey('tb_college.id'), nullable=False)

    classes = db.relationship("Class", backref="tb_major")

    def __repr__(self):
        return "[专业 %r]" % self.name

    pass


class Subject(db.Model):
    __tablename__ = "tb_subject"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(16), nullable=False)

    plans = db.relationship("Plan", backref="tb_subject")
    tests = db.relationship("Test", backref="tb_subject")

    def __repr__(self):
        return "[学科 %r]" % self.name

    pass


classes_plans = db.Table("classes_plans",
                         db.Column("plan_id", db.Integer, db.ForeignKey("tb_plan.id")),
                         db.Column("class_id", db.Integer, db.ForeignKey("tb_class.id"))
                         )

students_plans = db.Table("students_plans",
                          db.Column("plan_id", db.Integer, db.ForeignKey("tb_plan.id")),
                          db.Column("student_id", db.Integer, db.ForeignKey("tb_student.id"))
                          )


class Plan(db.Model):
    __tablename__ = "tb_plan"
    id = db.Column(db.Integer, primary_key=True)
    id_subject = db.Column(db.Integer, db.ForeignKey('tb_subject.id'), nullable=False)
    page_structure = db.Column(db.String(128), nullable=False)
    level = db.Column(db.Integer, default=5)
    date = db.Column(db.Date, nullable=False)
    time_start = db.Column(db.Time, nullable=False)
    time_length = db.Column(db.Integer, nullable=False)
    pages = db.relationship('Page', backref="tb_plan")
    classes = db.relationship('Class',
                              secondary=classes_plans,
                              backref=db.backref("tb_plan"))
    tested_students = db.relationship('Student',
                                      secondary=students_plans,
                                      backref=db.backref("tb_plan"))

    def __repr__(self):
        return "[考试计划 %r]" % self.id

    pass


class Page(db.Model):
    __tablename__ = "tb_page"
    id = db.Column(db.Integer, primary_key=True)
    id_plan = db.Column(db.Integer, db.ForeignKey('tb_plan.id'), nullable=False)
    id_student = db.Column(db.Integer, db.ForeignKey('tb_student.id'), nullable=False)
    content = db.Column(db.String(1024), nullable=False)
    answer = db.Column(db.Text, nullable=True)
    rest_time = db.Column(db.Integer, nullable=True)
    code = db.Column(db.Integer, nullable=True)

    def __repr__(self):
        return "[试卷 %r]" % self.id

    pass


class Test(db.Model):
    __tablename__ = "tb_test"
    id = db.Column(db.Integer, primary_key=True)
    id_subject = db.Column(db.Integer, db.ForeignKey('tb_subject.id'), nullable=False)
    type = db.Column(db.Integer, db.ForeignKey('tb_test_type.id'), nullable=False)
    question = db.Column(db.VARCHAR(1024), nullable=False)
    answer = db.Column(db.VARCHAR(1000), nullable=False)
    level = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return "[试题 %r]" % self.id

    pass


class Class(db.Model):
    __tablename__ = "tb_class"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), nullable=False)
    id_major = db.Column(db.Integer, db.ForeignKey('tb_major.id'), nullable=False)

    students = db.relationship("Student", backref="tb_class")

    def __repr__(self):
        return "[%r]" % self.name

    pass


class TestType(db.Model):
    __tablename__ = "tb_test_type"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), nullable=False)

    tests = db.relationship("Test", backref="tb_test_type")

    def __repr__(self):
        return "[%r]" % self.name

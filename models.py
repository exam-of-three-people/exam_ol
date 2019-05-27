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
    id = db.Column(db.BigInteger, primary_key=True)
    name = db.Column(db.String(10), nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    grade = db.Column(db.Integer, nullable=False)
    class_id = db.Column(db.Integer, db.ForeignKey('tb_class.id'), nullable=False)

    subjects = db.relationship("StudentSubject", back_populates="student_association")
    student_subjects = db.relationship("StudentSubject", back_populates="student")

    @property
    def password(self):
        return AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def checkPassword(self, password):
        return check_password_hash(self.password_hash, password)

    def get_pages(self):
        pages = []
        for student_subject in self.student_subjects:
            for teacher_s_s in student_subject.teacher_s_ss:
                pages.extend(teacher_s_s.pages)
        return pages

    def get_current_page(self):
        for student_subject in self.student_subjects:
            for teacher_s_s in student_subject.teacher_s_ss:
                for page in teacher_s_s.pages:
                    if page.ongoing:
                        return page
        return None


    def __repr__(self):
        return "[学生 %r]" % self.id

    pass


class TeacherSS(db.Model):
    __tablename__ = "tb_teacher_s_s"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    student_subject_id = db.Column(db.Integer, db.ForeignKey("tb_student_subject.id"), primary_key=True)
    teacher_id = db.Column(db.BigInteger, db.ForeignKey("tb_teacher.id"), primary_key=True)

    student_subject_association = db.relationship("StudentSubject", back_populates="teachers")
    teacher_association = db.relationship("Teacher", back_populates="student_subjects")

    student_subject = db.relationship("StudentSubject", back_populates="teacher_s_ss")
    teacher = db.relationship("Teacher", back_populates="teacher_s_ss")

    pages = db.relationship("Page", back_populates="teacher_s_s")


class StudentSubject(db.Model):
    __tablename__ = "tb_student_subject"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    student_id = db.Column(db.BigInteger, db.ForeignKey("tb_student.id"), primary_key=True)
    subject_id = db.Column(db.Integer, db.ForeignKey("tb_subject.id"), primary_key=True)

    subject_association = db.relationship("Subject", back_populates="students")
    student_association = db.relationship("Student", back_populates="subjects")

    subject = db.relationship("Subject", back_populates="student_subjects")
    student = db.relationship("Student", back_populates="student_subjects")

    teachers = db.relationship("TeacherSS", back_populates="student_subject_association")
    teacher_s_ss = db.relationship("TeacherSS", back_populates="student_subject")


class Teacher(db.Model):
    __tablename__ = "tb_teacher"
    id = db.Column(db.BigInteger, primary_key=True)
    name = db.Column(db.String(10), nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    student_subjects = db.relationship("TeacherSS", back_populates="teacher_association")

    teacher_s_ss = db.relationship("TeacherSS", back_populates="teacher")

    def checkPassword(self, password):
        return check_password_hash(self.password_hash, password)

    def setPassword(self, password):
        self.password_hash = generate_password_hash(password)

    def get_pages(self):
        pages = []
        for teacher_s_s in self.teacher_s_ss:
            pages.extend(teacher_s_s.pages)
        return pages

    def __repr__(self):
        return "[%r老师]" % self.name

    pass


class College(db.Model):
    __tablename__ = "tb_college"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(16), nullable=False)

    majors = db.relationship("Major", backref="college")

    def __repr__(self):
        return "[学院 %r]" % self.name


class Major(db.Model):
    __tablename__ = "tb_major"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(16), nullable=False)
    college_id = db.Column(db.Integer, db.ForeignKey('tb_college.id'), nullable=False)

    classes = db.relationship("Class", backref="major")

    def __repr__(self):
        return "[专业 %r]" % self.name


class Subject(db.Model):
    __tablename__ = "tb_subject"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(16), nullable=False)

    tests = db.relationship("Test", backref="subject")
    students = db.relationship("StudentSubject", back_populates="subject_association")
    student_subjects = db.relationship("StudentSubject", back_populates="subject")

    def __repr__(self):
        return "[学科 %r]" % self.name


class Page(db.Model):
    __tablename__ = "tb_page"
    id = db.Column(db.Integer, primary_key=True)
    structure = db.Column(db.String(128), nullable=False)
    level = db.Column(db.Integer, default=2)
    date = db.Column(db.Date, nullable=False)
    time_start = db.Column(db.Time, nullable=False)
    time_length = db.Column(db.Integer, nullable=False)
    content = db.Column(db.String(1024), nullable=True)
    answer = db.Column(db.Text, nullable=True)
    ongoing = db.Column(db.Boolean, default=False)
    finished = db.Column(db.Boolean, default=False)
    rest_time = db.Column(db.Integer, nullable=True)
    code = db.Column(db.Integer, nullable=True)

    teacher_s_s_id = db.Column(db.Integer, db.ForeignKey("tb_teacher_s_s.id"))
    teacher_s_s = db.relationship("TeacherSS", back_populates="pages")

    def __repr__(self):
        return "[试卷 %r]" % self.id


class Test(db.Model):
    __tablename__ = "tb_test"
    id = db.Column(db.Integer, primary_key=True)
    subject_id = db.Column(db.Integer, db.ForeignKey('tb_subject.id'), nullable=False)
    type_ = db.Column(db.String(50), nullable=False)
    question = db.Column(db.VARCHAR(1024), nullable=False)
    answer = db.Column(db.VARCHAR(1000), nullable=False)
    level = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return "[试题 %r]" % self.id


class Class(db.Model):
    __tablename__ = "tb_class"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), nullable=False)
    major_id = db.Column(db.Integer, db.ForeignKey('tb_major.id'), nullable=False)

    students = db.relationship("Student", backref="class_")

    def __repr__(self):
        return "[%r]" % self.name

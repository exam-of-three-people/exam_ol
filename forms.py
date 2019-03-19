from flask_wtf import FlaskForm
from wtforms import SelectField, StringField, SubmitField, PasswordField, DateTimeField, BooleanField, TimeField, \
    DateField, SelectMultipleField
from wtforms.validators import DataRequired, EqualTo


class LoginForm(FlaskForm):
    id = StringField(label="学工号", validators=[DataRequired(message="id is None")])
    role = SelectField(coerce=int, choices=[(1, '学生'), (2, '教师')])
    remember_me = BooleanField(label="记住密码", default=False)
    password = PasswordField(label='密码', validators=[DataRequired(message="password is None")])
    login = SubmitField(label="登录")
    pass


class RegisterFormStudent(FlaskForm):
    id = StringField(u'学号', validators=[DataRequired()])
    name = StringField(u'姓名', validators=[DataRequired()])
    college = SelectField(u'学院', validators=[DataRequired()])
    major = SelectField(u'专业', validators=[DataRequired()])
    grade = SelectField(u'年级', validators=[DataRequired()])
    classes = SelectField(u'班级', validators=[DataRequired()])
    password = PasswordField(u'密码', validators=[DataRequired()])
    ensure_password = PasswordField(u'确认密码', validators=[DataRequired(), EqualTo('password', message=u'两次输入密码不一致！')])
    submit = SubmitField(u'提交')
    pass


class RegisterFormTeacher(FlaskForm):
    id = StringField(u'工号', validators=[DataRequired()])
    name = StringField(u'姓名', validators=[DataRequired()])
    password = PasswordField(u'密码', validators=[DataRequired()])
    ensure_password = PasswordField(u'确认密码', validators=[DataRequired(), EqualTo('password', message=u'两次输入密码不一致！')])
    submit = SubmitField(u'提交')
    pass


class StudentInfoForm(FlaskForm):
    id = StringField(u'学号', validators=[DataRequired()])
    name = StringField(u'姓名', validators=[DataRequired()])
    college = SelectField(u'学院', validators=[DataRequired()])
    major = SelectField(u'专业', validators=[DataRequired()])
    grade = SelectField(u'年级', validators=[DataRequired()])
    classes = SelectField(u'班级', validators=[DataRequired()])
    pre_password = PasswordField(u'原密码')
    new_password = PasswordField(u'新密码')
    ensure_password = PasswordField(u'确认密码', validators=[EqualTo('password', message=u'两次输入密码不一致！')])
    submit = SubmitField(u'保存')
    pass


class TeacherInfoForm(FlaskForm):
    id = StringField(u'工号', validators=[DataRequired()])
    name = StringField(u'姓名', validators=[DataRequired()])
    pre_password = PasswordField(u'原密码')
    new_password = PasswordField(u'新密码')
    ensure_password = PasswordField(u'确认密码')
    submit = SubmitField(u'保存')
    pass


class TestCreaterForm(FlaskForm):
    date = DateField(u'日期', validators=[DataRequired()], render_kw={"type": "date"})
    start_time = TimeField(u'开始时间', validators=[DataRequired()], render_kw={"type": "Time"})
    end_time = TimeField(u'结束时间', validators=[DataRequired()], render_kw={"type": "Time"})
    subject = SelectField(u'科目', validators=[DataRequired()], choices=[(1, '1'), (2, '2')])
    class_ = SelectMultipleField(u'班级', validators=[DataRequired()], choices=[(1, '1'), (2, '2')])
    submit = SubmitField(u'创建')
    pass

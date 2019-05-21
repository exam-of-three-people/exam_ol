from flask_wtf import FlaskForm
from wtforms import SelectField, StringField, SubmitField, PasswordField, DateTimeField, BooleanField, TimeField, \
    DateField, SelectMultipleField, IntegerField
from wtforms.validators import DataRequired, EqualTo, InputRequired


class LoginForm(FlaskForm):
    id = StringField(label="学工号", validators=[DataRequired(message="id is None")],
                     render_kw={"type": "number", "min": "1", "max": "99999999999"})
    role = SelectField(label="身份", coerce=int, choices=[(1, '学生'), (2, '教师')])
    remember_me = BooleanField(label="记住密码", default=False)
    password = PasswordField(label='密码', validators=[DataRequired(message="password is None")])
    login = SubmitField(label="登　　录",render_kw={"style": "width:137%"})
    pass


class RegisterFormStudent(FlaskForm):
    id = StringField(u'学号', validators=[DataRequired()], render_kw={"type": "number", "min": "1", "max": "99999999999"})
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
    id = StringField(u'工号', validators=[DataRequired()], render_kw={"type": "number", "min": "1", "max": "99999999999"})
    name = StringField(u'姓名', validators=[DataRequired()])
    password = PasswordField(u'密码', validators=[DataRequired()])
    ensure_password = PasswordField(u'确认密码', validators=[DataRequired(), EqualTo('password', message=u'两次输入密码不一致！')])
    submit = SubmitField(u'提交')
    pass


class StudentInfoForm(FlaskForm):
    id = StringField(u'学号', validators=[DataRequired()], render_kw={"type": "number", "min": "1", "max": "99999999999"})
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
    id = StringField(u'工号', validators=[DataRequired()], render_kw={"type": "number", "min": "1", "max": "99999999999"})
    name = StringField(u'姓名', validators=[DataRequired()])
    pre_password = PasswordField(u'原密码')
    new_password = PasswordField(u'新密码')
    ensure_password = PasswordField(u'确认密码')
    submit = SubmitField(u'保存')
    pass


class TestCreaterForm(FlaskForm):
    date = DateField(u'日期', validators=[DataRequired()], render_kw={"type": "date"})
    start_time = TimeField(u'开始时间', validators=[DataRequired()], render_kw={"type": "time"})
    time_length = TimeField(u'持续时间', validators=[DataRequired()], render_kw={"type": "time"})
    subject = SelectField(u'科目', validators=[DataRequired()], choices=[(1, '1'), (2, '2')])
    class_ = SelectMultipleField(u'班级', validators=[DataRequired()], choices=[(1, '1'), (2, '2')])
    choice_question_number = IntegerField(u'选择题个数', validators=[InputRequired()],
                                          render_kw={"type": "number", "min": "0", "max": "1000"})
    fill_blank_question_number = IntegerField(u'填空题个数', validators=[DataRequired()],
                                              render_kw={"type": "number", "min": "0", "max": "1000"})
    true_false_question_number = IntegerField(u'判断题个数', validators=[DataRequired()],
                                              render_kw={"type": "number", "min": "0", "max": "1000"})
    free_response_question_number = IntegerField(u'大题个数', validators=[DataRequired()],
                                                 render_kw={"type": "number", "min": "0", "max": "1000"})
    level = IntegerField(u'考试难度', validators=[DataRequired], render_kw={"type": "number", "min": "1", "max": "3"})
    submit = SubmitField(u'创建')
    pass

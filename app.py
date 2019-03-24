from flask_script import Manager
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from models import Student, Teacher, College, Major, Subject, Plan, Page, Test, Class, TestType, db
from flask_migrate import Migrate, MigrateCommand
from flask_admin.form import BaseForm
from wtforms import StringField
from views import app
from wtforms.validators import DataRequired, EqualTo
from flask_bootstrap import Bootstrap

bootstrap = Bootstrap()
bootstrap.init_app(app)
app.config['BOOTSTRAP_SERVE_LOCAL'] = True

migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)

admin = Admin()
admin.init_app(app)


class IdBrandForm(BaseForm):
    id = StringField(validators=[DataRequired()])


class IdBrandModelView(ModelView):
    column_display_pk = True
    form_base_class = IdBrandForm


admin.add_view(IdBrandModelView(Student, db.session))
admin.add_view(IdBrandModelView(Teacher, db.session))
admin.add_view(ModelView(College, db.session))
admin.add_view(ModelView(Major, db.session))
admin.add_view(ModelView(Subject, db.session))
admin.add_view(ModelView(Plan, db.session))
admin.add_view(ModelView(Page, db.session))
admin.add_view(ModelView(Test, db.session))
admin.add_view(ModelView(Class, db.session))
admin.add_view(ModelView(TestType, db.session))

if __name__ == '__main__':
    manager.run()

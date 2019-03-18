from flask_script import Manager
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from models import Student, Teacher, College, Major, Subject, Plan, Page, Test, Class, TestType, db
from flask_migrate import Migrate, MigrateCommand
from flask_admin.form import BaseForm
from wtforms import StringField
from views import app

migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)

admin = Admin()
admin.init_app(app)


class IdBrandForm(BaseForm):
    id = StringField()


class IdBrandModelView(ModelView):
    column_display_pk = True
    form_base_class = IdBrandForm


admin.add_view(IdBrandModelView(Student, db.session))
admin.add_view(IdBrandModelView(Teacher, db.session))
admin.add_view(IdBrandModelView(College, db.session))
admin.add_view(IdBrandModelView(Major, db.session))
admin.add_view(IdBrandModelView(Subject, db.session))
admin.add_view(IdBrandModelView(Plan, db.session))
admin.add_view(IdBrandModelView(Page, db.session))
admin.add_view(IdBrandModelView(Test, db.session))
admin.add_view(IdBrandModelView(Class, db.session))
admin.add_view(IdBrandModelView(TestType, db.session))

if __name__ == '__main__':
    manager.run()

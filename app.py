from views import app
from flask_script import Manager
from flask_login import login_required, current_user, LoginManager
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from models import app, Student, Teacher, College, Major, Subject, Plan, Page, Test, Class, TestType, db
from flask_migrate import Migrate, MigrateCommand

migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)

login_manager = LoginManager()
login_manager.init_app(app)

admin = Admin()
admin.init_app(app)

admin.add_view(ModelView(Student, db.session))
admin.add_view(ModelView(Teacher, db.session))
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

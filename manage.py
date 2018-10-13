# encoding=utf-8
import os
from app import create_app
from app.models.models import *
from app.models.role import Role
from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand

# 从环境变量中读取config否则设置为default
from app.models.users import User

# app = create_app(os.getenv('FLASK_CONFIG') or 'default')
app = create_app("development")
COV = None
if os.environ.get("FLASK_COVERAGE"):
    import coverage

    COV = coverage.coverage(branch=True, include="app/*")
    COV.start()

manager = Manager(app)
migrate = Migrate(app, db)


@manager.command
def test(coverage=False):
    # 如果环境变量中没有
    if coverage and not os.environ.get("FLASK_COVERAGE"):
        import sys

        os.environ["FLASK_COVERAGE"] = "1"
        os.execvp(sys.executable, [sys.executable] + sys.argv)

    import unittest

    tests = unittest.TestLoader().discover("tests")
    unittest.TextTestRunner(verbosity=2).run(tests)
    if COV:
        COV.stop()
        COV.start()
        print("COVERate Summary:")
        COV.report()
        basedir = os.path.abspath(os.path.dirname(__file__))
        covdir = os.path.join(basedir, "tmp/coverage")
        COV.html_report(directory=covdir)
        print("html version: file://%s/index.html" % covdir)
        COV.erase()


@manager.command
def profile(length=25, profile_dir=None):
    from werkzeug.contrib.profiler import ProfilerMiddleware

    app.wsgi_app = ProfilerMiddleware(
        app.wsgi_app, restrictions=[length], profile_dir=profile_dir
    )
    app.run()


@manager.command
def deploy():
    from flask_migrate import upgrade
    from app.models.users import Role, User

    upgrade()

    # 创建表
    Role.insert_roles()
    # 建立自连接
    User.add_self_follows()


def make_shell_context():
    dicts = {
        "app": app,
        "db": db,
        "User": User,
        "Role": Role,
        "Post": Post,
        "Task": Task,
        "Message": Message,
        "Notification": Notification,
    }
    return dicts


manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command("db", MigrateCommand)

if __name__ == "__main__":
    manager.run()

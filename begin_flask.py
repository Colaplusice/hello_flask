# encoding=utf-8
import os
from hello import *
from flask import Flask, render_template, redirect, url_for, session, flash
from flask import make_response
from flask_migrate import Migrate, MigrateCommand
from flask_moment import Moment
from flask_wtf import Form
from flask_script import Shell
from wtforms import StringField, SubmitField
from wtforms.validators import Required
from flask_bootstrap import Bootstrap
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from app.models import *

# __file__='/Users/fanjialiang2401/Desktop/django_1/VENV_scrapy/hello_flask/sql'
base_dir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
from flask_mail import Mail, Message

mail = Mail(app)
migrate = Migrate(app, db)
app.config['SECRET_KEY'] = 'hard to gess string'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(base_dir,
                                                                    'data.sqlite')
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['MAIL_SERVER'] = 'smtp.163.com'
app.config['MAIL_PORT'] = '25'
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get('name_1')
app.config['MAIL_PASSWORD'] = os.environ.get('gpassword')

db = SQLAlchemy(app)

moment = Moment(app)
bootstrap = Bootstrap(app)


# 跨站点伪造

class nameForm(Form):
    name = StringField('what is you name', validators=[Required()])
    submit = SubmitField('submit')


@app.route('/', methods=['GET', 'POST'])
def index():
    form = nameForm()
    name = None
    if form.validate_on_submit():
        oldname = session.get('name')
        sd = User.query.filter_by(username=oldname).first()
        if sd is None:
            session['msg'] = '用户已被注册'
        else:
            user_role = Role.query.filter_by(name='user').first()
            new_user = User(username=oldname, role=user_role)
            db.session.add(new_user)
            db.session.commit(True)
            session['msg'] = '注册成功'
        # 新数据为表单数据，旧数据为session中的数据
        if oldname is not None and oldname != form.name.data:
            flash('你改名字了')
        # 更新session的值
        session['name'] = form.name.data
        return redirect(url_for('index'))
    return render_template('index.html', current_time=datetime.utcnow(),
                           form=form, name=session.get('name'))


@app.route('/user/<name>')
def user(name):
    return render_template('user.html', name=name)


def make_shell_context():
    return dict(app=app, db=db, User=User, Role=Role)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.route('/base')
def base():
    return render_template('base.html')


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


from flask_script import Manager

manager = Manager(app)

# 增加回调
manager.add_command('shell', Shell(make_context=make_shell_context()))


class NameForm(Form):
    name = StringField('what is your name?', validators=[Required()])
    submit = SubmitField('Submit')


@app.route('/send')
def send():
    print('调用了send方法')
    msg = Message('tests subject', sender='fjl2401@163.com')
    rece = ['995972493@qq.com']
    msg.body = 'tests body'
    msg.html = '<b>Html</b> body'

    with app.app_context():
        mail.send(msg)


# 数据库模型

# send()

if __name__ == '__main__':
    # app.run(debug=True)
    # send()
    manager.run()

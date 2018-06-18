# encoding=utf-8
from flask_mail import Mail, Message
from flask import Flask, render_template, redirect, url_for, session, flash
from flask_moment import Moment
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from config import config
from flask_pagedown import PageDown

bootstrap = Bootstrap()
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'
mail = Mail()
moment = Moment()
db = SQLAlchemy()
pagedown = PageDown()


# 工厂函数
def create_app(config_name):
    app = Flask(__name__)

    app.config.from_object(config[config_name])
    bootstrap.init_app(app)
    mail.init_app(app)
    moment.init_app(app)
    login_manager.init_app(app)
    db.init_app(app)
    pagedown.init_app(app)
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')
    # error

    # 注册蓝本
    from .api_1_0 import api as api_1_0_blueprint
    app.register_blueprint(api_1_0_blueprint, url_prefix='/api/')

    return app

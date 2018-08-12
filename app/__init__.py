# encoding=utf-8
from flask_mail import Mail
from flask import Flask
from flask_moment import Moment
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from configs import config
from flask_pagedown import PageDown
from redis import Redis
import rq
import logging
from logging.handlers import RotatingFileHandler
import os

dir_name = os.path.dirname(__file__)
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
    app.redis = Redis.from_url(app.config['REDIS_URL'])
    # 提交任务的队列
    app.task_queue = rq.Queue('hello_flask-tasks', connection=app.redis)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')
    # error

    # 配置log 在非debug情形下
    if not app.debug:
        basedir = os.path.abspath(os.path.dirname(__file__))
        log_dir = os.path.join(basedir, 'logs')
        if not os.path.exists(log_dir):
            os.mkdir(log_dir)
        file_handler = RotatingFileHandler(
            os.path.join(log_dir, 'hello_flask.log'),
            maxBytes=10240, backupCount=10)
        file_handler.setFormatter(
            logging.Formatter('%(asctime)s %(levelname)s: %'
                              '(message)s[in %(pathname)s:%(lineno)d]'))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)
        app.logger.setLevel(logging.INFO)
        app.logger.info('hello_flask start up')

    # 注册蓝本
    from .api_1_0 import api as api_1_0_blueprint
    app.register_blueprint(api_1_0_blueprint, url_prefix='/api/')

    return app

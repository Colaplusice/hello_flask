from flask import Flask
from redis import Redis
from app.extensions import *
# import rq
# import logging
# from logging.handlers import RotatingFileHandler
import os

dir_name = os.path.dirname(__file__)

login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'


def update_celery(app, celery):
    celery.conf.update(app.config)
    TaskBase = celery.Task
    class ContextTask(TaskBase):
        abstract = True
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)

    celery.Task = ContextTask


# 工厂函数
def create_app(config_name):
    app = Flask(__name__)
    # print('app name is {}'.format(app.name))
    app.config.from_pyfile('../configs/celery_config.py')
    app.config.from_object(config[config_name])
    bootstrap.init_app(app)
    mail.init_app(app)
    moment.init_app(app)
    login_manager.init_app(app)
    db.init_app(app)
    pagedown.init_app(app)
    app.redis = Redis.from_url(app.config['REDIS_URL'])
    # 提交任务的队列
    # app.task_queue = rq.Queue('hello_flask-tasks', connection=app.redis)
    app.config.from_pyfile('../configs/celery_config.py')
    update_celery(app, celery)
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')
    # error
    #
    # # 配置log 在非debug情形下
    # if not app.debug:
    #     basedir = os.path.abspath(os.path.dirname(__file__))
    #     log_dir = os.path.join(basedir, 'logs')
    #     if not os.path.exists(log_dir):
    #         os.mkdir(log_dir)
    #     file_handler = RotatingFileHandler(
    #         os.path.join(log_dir, 'hello_flask.log'),
    #         maxBytes=10240, backupCount=10)
    #     file_handler.setFormatter(
    #         logging.Formatter('%(asctime)s %(levelname)s: %'
    #                           '(message)s[in %(pathname)s:%(lineno)d]'))
    #     file_handler.setLevel(logging.INFO)
    #     app.logger.addHandler(file_handler)
    #     app.logger.setLevel(logging.INFO)
    #     app.logger.info('hello_flask start up')

    # 注册蓝本
    from .api_1_0 import api as api_1_0_blueprint
    app.register_blueprint(api_1_0_blueprint, url_prefix='/api/')

    from .play import play as play_blueprint
    app.register_blueprint(play_blueprint, url_prefix='/play/')

    return app

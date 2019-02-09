import os
from elasticsearch import Elasticsearch
from flask import Flask
from redis import Redis
from app.extensions import pagedown, db, login_manager, mail, moment, celery
from configs import config

dir_name = os.path.dirname(__file__)

login_manager.session_protection = "strong"
login_manager.login_view = "auth.login"


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
def create_app(config_name=None):
    if not config_name:
        config_name = os.environ.get("FLASK_ENV")
    app = Flask(__name__)
    app.config.from_pyfile("../configs/celery_config.py")
    app.config.from_object(config[config_name])
    mail.init_app(app)
    moment.init_app(app)
    login_manager.init_app(app)
    db.init_app(app)
    pagedown.init_app(app)
    app.redis = Redis.from_url(app.config["REDIS_URL"])
    # 提交任务的队列
    # app.task_queue = rq.Queue('hello_flask-tasks', connection=app.redis)
    update_celery(app, celery)

    app.elasticsearch = (
        Elasticsearch([app.config["ELASTICSEARCH_URL"]])
        if app.config["ELASTICSEARCH_URL"]
        else None
    )

    from .main import main as main_blueprint

    app.register_blueprint(main_blueprint)

    from .auth import auth as auth_blueprint

    app.register_blueprint(auth_blueprint, url_prefix="/auth")
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
    from .api import api as api_blueprint

    app.register_blueprint(api_blueprint, url_prefix="/api")

    from .play import play as play_blueprint

    app.register_blueprint(play_blueprint, url_prefix="/play")
    app.app_context().push()
    return app

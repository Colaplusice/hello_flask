#encoding=utf-8
import os

base_dir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = 'hard to gess string'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    FLASKY_MAIL_SUBJECT_PREFIX = '[Flasky]'
    FLASKY_MAIL_SENDER = 'fjl <fjl2401@163.com>'
    FLASKY_ADMIN = 'fjl2401@163.com'
    FLASKY_POSTS_PER_PAGE = 5
    FLASKY_USER_PER_PAGE = 10
    FLASKY_COMMENTS_PRE_PAGE = 5
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    FLASKY_SLOW_DB_QUERY_TIME=0.5
    MAIL_SERVER = 'smtp.163.com'
    SQLALCHEMY_RECORD_QUERIES = True
    MAIL_PORT = '25'
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('name_1')
    MAIL_PASSWORD = os.environ.get('gpassword')
    @staticmethod
    def init_app(app):
        pass


class DevelopementConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABSE_URL') or \
                              'sqlite:///' + os.path.join(base_dir, 'data.sqlite')
    DEBUG = True


class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABSE_URL') or \
                              'sqlite:///' + os.path.join(base_dir, 'data-tests.sqlite')
    WTF_CSRF_ENABLED = False


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
                              'sqlite:///' + os.path.join(base_dir, 'data.sqlite')


config = {
    'developement': DevelopementConfig,
    'testing': TestConfig,
    'production': ProductionConfig,
    'default': DevelopementConfig,
}

class ProductionConfig(Config):
    @classmethod
    def init_app(cls,app):
        Config.init_app(app)

        #把错误信息发送给管理员
        import logging
        from logging.handlers import SMTPHandler
        credentials=None
        secure=None

        if getattr(cls,'MAIL_USERNAME',None) is not None:
            credentials=(cls.MAIL_USERNAME,cls.MAIL_PASSWORD)
            if getattr(cls,'MAIL_USER_TLS',None):
                secure=()

        mail_handler=SMTPHandler(
            mailhost=(cls.MAIL_SERVER,cls.MAIL_PORT),
            fromaddr=cls.FLASKY_MAIL_SENDER,
            toaddrs=[cls.FLASKY_ADMIN],
            subject=cls.FLASKY_MAIL_SUBJECT_PREFIX+'Application Error',
            credentials=credentials,
            secure=secure
        )
        mail_handler.setLevel(logging.ERROR)
        app.logger.addHandler(mail_handler)


class UnixConfig(ProductionConfig):
    @classmethod
    def init_app(cls,app):
        ProductionConfig.init_app(app)

        #写入系统日志 日志会写入 /var/log/messages
        import logging
        from logging.handlers import SysLogHandler
        syslog_handler=SysLogHandler()
        syslog_handler.setLevel(logging.WARNING)
        app.logger.addHandler(syslog_handler)


















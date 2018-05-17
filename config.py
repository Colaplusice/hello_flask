import os

base_dir = os.path.abspath(os.path.dirname(__file__))


class Config:

    SECRET_KEY = 'hard to gess string'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    FLASKY_MAIL_SUBJECT_PREFIX='[Flasky]'
    FLASKY_MAIL_SENDER='fjl <fjl2401@163.com>'
    FLASKY_ADMIN='fjl2401@163.com'
    FLASKY_POSTS_PER_PAGE=5
    FLASKY_USER_PER_PAGE=10
    FLASKY_COMMENTS_PER_PAGE=5


class DevelopementConfig(Config):
    MAIL_SERVER='smtp.163.com'
    MAIL_PORT = '25'
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('name_1')
    MAIL_PASSWORD = os.environ.get('gpassword')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABSE_URL') or\
                              'sqlite:///' + os.path.join(base_dir, 'data.sqlite')
    DEBUG=True

class TestConfig(Config):
    TESTING=True
    SQLALCHEMY_DATABASE_URI =os.environ.get('TEST_DATABSE_URL')or \
                             'sqlite:///' + os.path.join(base_dir, 'data-tests.sqlite')

class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')or \
                              'sqlite:///' + os.path.join(base_dir, 'data.sqlite')


config={
    'developement':DevelopementConfig,
    'testing':TestConfig,

    'production':ProductionConfig,
    'default':DevelopementConfig,


}

@ staticmethod
def init_app(app):
        pass

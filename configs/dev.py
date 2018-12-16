from .base import Config
import os


class DevelopementConfig(Config):
    base_dir = os.path.abspath(os.path.dirname(__file__))
    # SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABSE_URL') \
    #                           or 'sqlite:///' + os.path.join(base_dir, 'data.sqlite')
    # SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(base_dir, 'data.sqlite')
    SQLALCHEMY_DATABASE_URI = "mysql://root:newpass@{}:3306/hello_flask?charset=utf8mb4".format(
        Config.DB_HOST
    )
    # 'sqlite:///' + os.path.join(base_dir, 'data.sqlite')
    DEBUG = True

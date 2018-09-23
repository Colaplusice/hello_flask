from .base import Config
import os


class DevelopementConfig(Config):
    # SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABSE_URL') \
    #                           or 'sqlite:///' + os.path.join(base_dir, 'data.sqlite')
    # SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    SQLALCHEMY_DATABASE_URI = 'mysql://root:newpass@localhost:3305/hello_flask?charset=utf8mb4'
    # 'sqlite:///' + os.path.join(base_dir, 'data.sqlite')
    DEBUG = True

from .base import *

import os


class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "mysql://root:newpass@{}:3306/hello_flask_test?charset=utf8mb4".format(
        Config.DB_HOST
    )
    WTF_CSRF_ENABLED = False

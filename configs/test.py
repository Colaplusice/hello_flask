from .base import *

import os

class TestConfig(Config):
    TESTING = True
    # SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABSE_URL') \
    #                           or 'sqlite:///' + os.path.join(base_dir,
    #                                                          'data-tests.sqlite')
    WTF_CSRF_ENABLED = False

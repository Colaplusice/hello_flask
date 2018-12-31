from celery import Celery
from flask_bootstrap import Bootstrap
from flask_cache import Cache
from flask_login import LoginManager
from flask_mail import Mail
from flask_moment import Moment
from flask_pagedown import PageDown
from flask_sqlalchemy import SQLAlchemy

mail = Mail()
moment = Moment()
db = SQLAlchemy()
pagedown = PageDown()
login_manager = LoginManager()
bootstrap = Bootstrap()
cache = Cache(config={"CACHE_TYPE": "simple"})
celery = Celery(__name__)


# class Flask_env:
#     def __init__(self, app=None):
#         self.app = app
#         if app:
#             self.init_app(app)
#
#     def init_app(self, app):
#         if self.app is None:
#             self.app = app
#         env_file = os.path.join(os.getcwd(), ".env")
#         if not env_file:
#             raise FileNotFoundError(".env file not found")
#         self.__import_vars(env_file)
#
#     def __import_vars(self, env_file):
#         # read file
#         # parse the str
#         # write in config
#         print("load .env file from parent dir")
#         with open(env_file) as opener:
#             lines = opener.readlines()
#             for line in lines:
#                 line = line.replace("'", "")
#                 line = line.strip("\n")
#                 # export
#                 if not line:
#                     continue
#                 if line.split(" ")[0] is "export":
#                     line = line.split(" ")[1]
#                 config_list = line.split("=")
#                 key, value = config_list[0], config_list[1]
#                 if self.app.config.get(key):
#                     print(
#                         "overwrite an exist key : {} {} ---> {}".format(
#                             key, self.app.config[key], value
#                         )
#                     )
#                 if value.isdigit():
#                     value = int(value)
#                 self.app.config[key] = value
#
#
# flask_env = Flask_env()

from flask_moment import Moment
from flask_mail import Mail
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from configs import config
from flask_cache import Cache
from flask_pagedown import PageDown
from flask_bootstrap import Bootstrap
from celery import Celery

mail = Mail()
moment = Moment()
db = SQLAlchemy()
pagedown = PageDown()
login_manager = LoginManager()
bootstrap = Bootstrap()
cache = Cache(config={'CACHE_TYPE': 'simple'})
celery=Celery(__name__)


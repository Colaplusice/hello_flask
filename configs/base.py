import os
from datetime import timedelta

base_dir = os.path.abspath(os.path.dirname(__file__))


class Config:
    TZ = "Asia/Shanghai"
    SECRET_KEY = "hard to gess string"

    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    ELASTICSEARCH_URL = "localhost:9200"

    DB_HOST = os.environ.get("DB_HOST", "localhost")
    POSTS_PER_PAGE = 5
    FLASKY_USER_PER_PAGE = 10
    FLASKY_COMMENTS_PRE_PAGE = 5
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    FLASKY_SLOW_DB_QUERY_TIME = 0.5
    MAIL_SERVER = "smtp.163.com"
    SQLALCHEMY_RECORD_QUERIES = True
    MAIL_PORT = "25"
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get("name_1")
    MAIL_PASSWORD = os.environ.get("gpassword")
    REDIS_URL = os.environ.get("REDIS_URL") or "redis://redis:6379"

    CACHE_BACKEND = "Redis"
    CACHE_PREFIX = "hello_flask"
    CACHE_HOST = "redis"
    CACHE_DB = 0
    CACHE_PORT = 6379

    LONG_CACHE_TTL = 24 * 60 * 60
    SHORT_CACHE_TTL = 10 * 60

    SEND_FILE_MAX_AGE_DEFAULT = timedelta(seconds=1)

    JAVASCRIPT = """
    alert('asd')  
    (function(){
var d=document,i=new Image,e=encodeURIComponent;
    
    i.src='%s/a.gif?url='+e(d.location.href)+'&ref='+e(d.referrer)+'&t='+e(d.title);
    })()
    """.replace(
        "\n", ""
    )
    # import socket
    # DOMAIN = socket.gethostbyname(socket.gethostname())
    # DOMAIN = "baidu.com"
    from base64 import b64decode

    BEACON = b64decode("R0lGODlhAQABAIAAANvf7wAAACH5BAEAAAAALAAAAAABAAEAAAICRAEAOw==")

    # SERVER_NAME = "localhost"
    # 验证码
    RECAPTCHA_PUBLIC_KEY = "6LeYIbsSAAAAACRPIllxA7wvXjIE411PfdB2gt2J"
    RECAPTCHA_PRIVATE_KEY = "6LeYIbsSAAAAAJezaIq3Ft_hSTo0YtyeFG-JgRtu"
    RECAPTCHA_API_SERVER = "localhost"
    # RECAPTCHA_DATA_ATTRS = {'theme': 'dark'}

    def init_app(self, app):
        pass

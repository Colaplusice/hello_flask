import os

workers = int(os.environ.get('WORKERS_NUM', 4))

bind = '0.0.0.0:5000'

worker_class = 'sync'

timeout = 20

limit_request_line = 4096

limit_request_fields = 100

limit_request_field_size = 8190

graceful_timeout = 5

loglevel = 'warning'

if os.getenv('FLASK_ENV', 'development') == 'production':
    loglevel = 'warning'

proc_name = 'hello_flask'
basedir = os.path.abspath(os.path.dirname(__file__))
log_dir = os.path.join(basedir, 'logs')

accesslog_path=os.path.join(log_dir,'acesslog.log')
errorlog_path=os.path.join(log_dir,'errorlog.log')

if not os.path.exists(accesslog_path):
    with open(accesslog_path,'w'):
        pass
if not os.path.exists(errorlog_path):
    with open(errorlog_path,'w'):
        pass

accesslog = accesslog_path
errorlog = errorlog_path
#!/bin/bash
#set path for flask config
export DATABASE_URL='mysql://root:mysqlpass@localhost:3306/hello_flask?charset=utf8mb4'
export FLASK_CONFIG='production'
#导入邮箱账号之类的环境变量

python manage.py runserver --host 0.0.0.0



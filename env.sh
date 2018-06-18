#!/bin/bash
#set path for flask config
export DATABASE_URL='mysql://root:newpass@localhost:3306/hello_flask?charset=utf8mb4'
export FLASK_CONFIG='production'
export gname='fjl2401'
export gpassword='f15114826978f'
export password1='f15114826978f'
export name_1='fjl2401@163.com'

python manage.py runserver --host 0.0.0.0



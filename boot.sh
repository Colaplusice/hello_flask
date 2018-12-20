#!/usr/bin/env bash


run(){
    flask run -h 0.0.0.0 -p 5000
    #gunicorn -b  0.0.0.0:5000 --access-logfile - --error-logfile - manage:app
}

import_data(){
     mysql -uroot -pnewpass hello_flask < ~/hello_flask.sql
}

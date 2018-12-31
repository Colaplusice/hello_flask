#!/usr/bin/env bash

MYSQL_PASSWORD="newpass"
MYSQL_USERNAME="root"

setup_mysql(){
    
    shell/setup_mysql.sh start
    chmod +x ./boot_python.sh
    if [[ $? == "0" ]]; then
        echo "success"
    else  echo"false"
        exit $?
    fi
}
import_data(){
docker exec -i hello_flask_db_1 mysql -uroot -pnewpass  hello_flask < hello_flask.sql
}
setup_redis(){
    shell/setup_redis.sh start
    if [[ $? == "0" ]]; then
        echo "success"
    else  echo"false"
        exit $?
    fi
    
}

create_db(){
    echo create database "$1" CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci | mysql -u "$MYSQL_USERNAME" -p"$MYSQL_PASSWORD"
}

run(){
    docker-compose up
    import_data
}
action=$1
shift
case $action in
    create_db) create_db "$*"
    ;;
    run) run
    ;;
    import_data) import_data
    ;;
    *) echo default
    ;;
esac
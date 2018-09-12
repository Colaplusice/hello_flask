#!/bin/bash

USER_DIR="~"
USER="root"
PASS="newpass"
HOST="127.0.0.1"
PORT="3305"
DB_NAME="hello_flask"
DB_DATA=""

CURRENT_DIR=$(pwd)
BASE_DIR=(dirname $CURRENT_DIR)
SQL_DIR="$BASE_DIR/hello_flask_2018-08-23.sql"

CurDir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# get host ip



if [ "$(uname)"=="Darwin" ];
then
HostIP="$( osascript -e "IPv4 address of (system info)")"
 # Mac OS X 操作系统

elif [ "$(expr substr $(uname -s) 1 5)"=="Linux" ]; then
    HostIP= "$(ip route get 1 | awk '{print $NF;exit}')"
# GNU/Linux操作系统

fi


# set data dir
MyData=~/docker_data/mysql
MyLog=~/docker_mysql/mysql_log


check_non_empty() {
  # $1 is the content of the variable in quotes e.g. "$FROM_EMAIL"
  # $2 is the error message
  if [[ "$1" == "" ]]; then
    echo "ERROR: specify $2"
    exit -1
  fi
}

check_exec_success() {
  # $1 is the content of the variable in quotes e.g. "$FROM_EMAIL"
  # $2 is the error message
  if [[ "$1" != "0" ]]; then
    echo "ERROR: $2 failed"
    echo "$3"
    exit -1
  fi
}


update_images() {
  # pull mysql docker image
  docker pull mysql:5.6
  check_exec_success "$?" "pulling 'mysql' image"
}

start() {

  update_images

  docker kill mysql 2>/dev/null
  docker rm -v mysql 2>/dev/null


# 电脑地址和 docker容器地址映射
  docker run -d --name mysql \
    -v ${CURRENT_DIR}/conf:/etc/mysql/conf.d \
    -v ${MyData}:/var/lib/mysql \
    -v ${MyLog}:/var/log/mysql \
    -e MYSQL_ROOT_PASSWORD="$PASS" \
    -p 3305:3306\
    --log-opt max-size=10m \
    --log-opt max-file=9 \
    mysql:5.6

  check_exec_success "$?" "start mysql container"
}

stop() {
  docker stop mysql 2>/dev/null
  docker rm -v mysql 2>/dev/null
    check_exec_success "$?" "stop mysql container"

}

destroy() {
  stop
  rm -rf ${MyData}
  rm -rf ${MyLog}
  check_exec_success "$?" "remove all data"

}

createdb() {
  docker exec mysql mysql -u $USER -p$PASS -e "create database $1 CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"
[ $? -eq 0 ] && echo Created DB SUCCESS! || echo DB already exist
}

createdb(){
mysql -h $HOST -P $PORT  -u$USER -p$PASS <<EOF 2>/dev/null
CREATE DATABASE $DB_NAME;
EOF

}

dump_sql(){
db_name=$1
sql_file=$2



}


#################
# Start of script
#################

case "$1" in
  start) start ;;
  stop) stop ;;
  restart)
    stop
    start
    ;;
  destroy) destroy ;;
  dump_sql) dump_sql $1 $2;;
  createdb) createdb $2;;
  *)
    echo "Usage:"
    echo "./mysql.sh start|stop|restart"
    echo "./mysql.sh destroy"
    exit 1
    ;;
esac

exit 0
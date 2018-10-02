#!/bin/bash

USER_DIR="~"
USER="root"
PASS="newpass"
HOST='localhost'
PORT=3305
DB_NAME="hello_flask"

CURRENT_DIR=$(pwd)
BASE_DIR=($CURRENT_DIR)
SQL_DIR="$BASE_DIR/hello_flask.sql"

#CurDir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

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
MyData=~/docker_mysql/mysql
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


#cat ${CURRENT_DIR}/conf/my.cnf


# 电脑地址和 docker容器地址映射
  docker run -d --name mysql \
    -v ${CURRENT_DIR}/conf:/etc/mysql/conf.d \
    -v ${MyData}:/var/lib/mysql \
    -v ${MyLog}:/var/log/mysql \
    -e MYSQL_ROOT_PASSW ORD=newpass \
    -p 3305:3306 \
    --log-opt max-size=10m \
    --log-opt max-file=9 \
    mysql:5.6

  check_exec_success "$?" "start mysql container"
  # 导入数据
  sleep 3
  dump_sql
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

mysql -h $HOST -P $PORT  -u$USER -p$PASS <<EOF 2>/dev/null
CREATE DATABASE $DB_NAME CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
EOF

#  docker exec mysql mysql -h $HOST -p $PASS -u $USER  -e "create database $1 CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"
[ $? -eq 0 ] && echo Created DB SUCCESS! || echo DB already exist
}

#createdb(){

#}

# 导入sql数据
dump_sql(){
createdb $DB_NAME

#docker exec -i mysql mysql -h $HOST -p$PASS -uroot  hello_flask < $SQL_DIR

#docker exec -i mysql mysql -uroot -h 127.0.0.1 hello_flask < $SQL_DIR

mysql -u$USER -p$PASS -h $HOST -P $PORT  $DB_NAME < $SQL_DIR
if [[ $? == 0 ]]; then
echo "导入数据成功"
else
echo "导入数据失败，状态码为 $?"
exit $?
fi
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
  dump_sql) dump_sql ;;
  createdb) createdb $2;;
  *)
    echo "Usage:"
    echo "./mysql.sh start|stop|restart"
    echo "./mysql.sh destroy"
    exit 1
    ;;
esac

exit 0
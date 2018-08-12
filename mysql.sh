#!/bin/bash

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

CurDir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# get host ip
HostIP="$(ip route get 1 | awk '{print $NF;exit}')"

# set data dir
MyData=/data/mysql/data
MyLog=/data/mysql/logs

update_images() {
  # pull mysql docker image
  docker pull mysql:5.6

  check_exec_success "$?" "pulling 'mysql' image"
}

start() {

  update_images

  docker kill mysql 2>/dev/null
  docker rm -v mysql 2>/dev/null

  docker run -d --name mysql \
    -v ${CurDir}/conf:/etc/mysql/conf.d \
    -v ${MyData}:/var/lib/mysql \
    -v ${MyLog}:/var/log/mysql \
    -e MYSQL_ROOT_PASSWORD=newpass \
    --net=host \
    --log-opt max-size=10m \
    --log-opt max-file=9 \
    mysql:5.6

  check_exec_success "$?" "start mysql container"
}

stop() {
  docker stop mysql 2>/dev/null
  docker rm -v mysql 2>/dev/null
}

destroy() {
  stop
  rm -rf ${MyData}
  rm -rf ${MyLog}
}

createdb() {
  docker exec mysql mysql -u root -ptoor333666 -e "create database $1 CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"
}

##################
# Start of script
##################

case "$1" in
  start) start ;;
  stop) stop ;;
  restart)
    stop
    start
    ;;
  destroy) destroy ;;
  createdb) createdb $2;;
  *)
    echo "Usage:"
    echo "./mysql.sh start|stop|restart"
    echo "./mysql.sh destroy"
    exit 1
    ;;
esac

exit 0

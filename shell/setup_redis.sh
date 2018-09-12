#!/usr/bin/env bash




RedisData=~/docker_data/redis

start(){
update_image
docker kill redis 2>/dev/null
docker rm -v redis 2>/dev/null


docker run -d --name redis \
    -v ${RedisData}:/data \
    -p 6378:6379 \
    --log-opt max-size=10m \
    --log-opt max-file=9 \
    redis:4-alpine

  check_exec_success "$?" "start redis container"
}

update_image(){
docker pull redis:4-alpine
check_exec_success "$?"  "pulling redis image"
}

# 检测命令执行是否成功
check_exec_success(){
if [[ "$1" == "" ]]; then
echo "error: specify $2"
fi
}

stop(){
docker stop redis 2>/dev/null
doker rm -v redis 2>/dev/null
  check_exec_success "$?"  "stop redis container"

}

destroy(){
stop
rm -rf${RedisData}
}
case "$1" in
    start) start;;
    stop) stop;;
    destroy) destroy;;

esac




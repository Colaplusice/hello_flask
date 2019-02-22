#!/usr/bin/env bash

function run() {
   gunicorn -b  0.0.0.0:5000 --access-logfile - --error-logfile - run:app

}

function deploy() {
   ssh  ubuntu@111.231.82.45 "cd /home/ubuntu/flask_project/hello_flask; git pull"
   ssh  ubuntu@111.231.82.45 "cd /home/ubuntu/flask_project/hello_flask; /home/ubuntu/miniconda3/bin/docker-compose up -d --build"
}
Action=$1
shift
 case "$Action" in
 run)
    run ;;
 deploy)
    deploy;;
    *) echo 'usage:
     runserver: ./boot.sh run
     update code and deploy: ./boot.sh deploy' ;;
esac

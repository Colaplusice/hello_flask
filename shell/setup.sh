#!/usr/bin/env bash

#
#
#. /Users/fanjialiang2401/Anacoda/anaconda2/etc/profile.d/conda.sh conda activate hello_flask
#
#pip -V
#pip list
##pip install -r requirements/requirements.txt
#
#sh ./setup_mysql.sh create
#
#
#gunicorn -c gunicorn.py hello_flask:app
./setup_mysql.sh start

if [[ $? == "0" ]]; then
    echo "success"
else  echo"false"
exit $?
fi

./setup_redis.sh start
if [[ $? == "0" ]]; then
    echo "success"
else  echo"false"
exit $?
fi


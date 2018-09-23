#!/usr/bin/env bash
# @Time    : 2018/9/23 下午2:41

python3 -m venv ../../venv
source ../../venv/bin/activate

pip install --upgrade pip

pip install -r ../requirements/requirements.txt

export FLASK_CONFIG='production'


gunicorn -c ../gunicorn.py --chdir ../ -D hello_flask:app


if [ $? -eq 0 ]; then
echo run successful!
else
echo 'failed'

fi





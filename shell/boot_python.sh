#!/usr/bin/env bash
# @Time    : 2018/9/23 下午2:41

python3 -m venv ../../venv
source ../../venv/bin/activate

pip install --upgrade pip

pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -r ../requirements/requirements.txt

#export FLASK_CONFIG='production'

lsof -i:5000
if [ $? -eq 0 ];then
kill  `lsof -i:5000 | awk '{print $2}'`
fi

gunicorn -c ../gunicorn.py --chdir ../ -D hello_flask:app


if [ $? -eq 0 ]; then
echo run successful!
else
echo 'failed'

fi





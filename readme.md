# flask web开发书上的代码实现

## 包含一些功能扩充和修改

### 博客的地址 [IceCola的博客](http://111.231.82.45)

### 部署的方法

## 安装包

 pip install -U -r requirements/requirements -i https://mirrors.aliyun.com/pypi/simple
 pip install -U -r requirements/test_requirements.txt -i https://mirrors.aliyun.com/pypi/simple

在根目录下创建.env文件，然后配置flask config信息，添加到.gitignore（FLASK_DEBUG不能在.env中配置）
### example:

FLASK_ENV=development
ELASTICSEARCH_URL=http://localhost:9200
DB_PASSWORD=123456
FLASK_RUN_PORT=8000

## mysql用docker来部署

运行mysql.sh  sh mysql.sh start

## 线上部署和本地同步   

数据库确保一致
mysql 同步连接

## 数据同步:

python hello_flask.py db migrate
python hello_flask.py db upgrade

## 重构

增加gitignore文件

启动  gunicorn 启动
 
gunicorn -c gunicorn.py hello_flask:app

celery worker 运行
celery worker -A app.celery --loglevel=info
celery worker -A celery_worker.celery --loglevel=info


### 将项目通过docker发布出去

建立docker_compose file

  

### 终极指令

./
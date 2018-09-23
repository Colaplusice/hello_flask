# flask web开发书上的代码实现
## 包含一些功能扩充和修改

### 博客的地址 [IceCola的博客](http://111.231.82.45)

### 部署的方法
## 安装包
 pip install -U -r requirements/requirements -i https://mirrors.aliyun.com/pypi/simple
 pip install -U -r requirements/test_requirements.txt -i https://mirrors.aliyun.com/pypi/simple

## mysql用docker来部署

运行mysql.sh  sh mysql.sh start
 



数据库 写入环境变量
在bashrc文件中
source ~/.bashrc
export DATABASE_URL='mysql://root:newpass@111.231.82.45:3306/hello_flask?charset=utf8mb4'
export FLASK_CONFIG='production'
export gname='fjl2401'
export gpassword='f15114826978f'
export password1='f15114826978f'
export name_1='fjl2401@163.com'


## 线上部署和本地同步   
数据库确保一致
mysql 同步连接







数据同步:
python hello_flask db upgrade

## 重构

增加gitignore文件

启动  gunicorn 启动
 
gunicorn -c gunicorn.py hello_flask:app

celery worker 运行
celery worker -A app.celery --loglevel=info
celery worker -A celery_worker.celery --loglevel=info


### 在docker中运行python

写好dockerfile 
 docker build -t microblog:latest .
  docker build -t hello_flask .
  
### 终极指令
./
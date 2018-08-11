# flask web开发书上的代码实现
## 包含一些功能扩充和修改

### 博客的地址 [IceCola的博客](http://111.231.82.45)

#### 供大家学习和使用

### 部署的方法

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



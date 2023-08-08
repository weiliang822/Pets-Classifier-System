# 宠物识别系统
![avatar](login.jpg)
![avatar](preview.jpg)
### 技术栈
前端：Vue3、Typescript、Element Plus\
后端：Django\
数据库：MySQL\
爬虫：gevent+requests+beautifulsoup4\
深度学习模型：TensorFlow+DenseNet

#### 导入数据库

进入mysql安装目录的bin文件夹下（此处以本机为例）

```
cd C:\Program Files\MySQL\MySQL Server 8.0\bin
```

启动mysql

```
mysql -u 用户名 -p
```

创建数据库

```
create database pets_classifer_system;
```

使用数据库

```
use pets_classifer_system;
```

导入sql文件（注意指定sql文件路径）

```
source db.sql;
```

#### 后端启动

进入后端目录

```
cd pets_classifer_system
```

安装依赖

```
pip install -r requirements.txt
```

在settings.py中修改数据库信息

```
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": "pets_classifer_system",
        'PORT': 3306,  # 端口
        'HOST': '127.0.0.1',  # 改成本地ip
        'USER': '',  # 修改数据库用户名
        'PASSWORD': '',  # 修改数据库密码
    }
}
```

迁移数据库

```
py manage.py makemigrations
py manage.py migrate
```

启动后端服务器

```
py manage.py runserver 0.0.0.0:8000
```

注册管理员

```
py manage.py createsuperuser
```

#### 前端启动

进入前端目录

```
cd frontend
```

安装依赖

```
npm install
```

启动前端服务器

```
npm run serve
```

#### 爬虫和训练

进入目录

```
cd pets_classify
```

安装依赖

```
pip install -r requirements.txt
```

启动爬虫

```
python spider.py
```

训练模型

```
python models.py
python train.py
```

#### 参考项目
https://github.com/AaronJny/pets_classifer

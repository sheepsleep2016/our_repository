pip install pycryptodome xlrd  安装这两个模块，其他的根据提示来安装，
需要导入数据，数据：一个是excel中的数据，一个是物品的图片，（有导入的相关模块）

先要在mysql数据库里面建立名称为xianyudb的数据库，建库语句：
create database xianyudb default charset utf8 collate uhf8_general_ci;

然后进入manage.py所在的文件夹，输入：./manage.py migrate
此时会在库中建表

输入：./manage.py createsuperuser 
一直按ENTER，直到设置密码，默认用户名是tarena

导入数据：
这个比较复杂，要是啥时候有时间我帮你处理一下吧

要导入数据之后主页才会有物品显示。

在manage.py所在的文件夹，输入：./manage.py runserver是启动服务
然后在浏览器输入127.0.0.1：8000就可以进入主页了


目前实现的页面功能：
注册/登录/忘记密码
主页、商品页、购买页、物品上架页
个人中心：个人信息页、修改密码、上架的物品、历史订单
网站反馈、订单反馈、关于网站、团队介绍（最终版不在我这儿，只是个模板）



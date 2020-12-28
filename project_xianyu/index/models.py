from django.db import models
from django.core.files.storage import FileSystemStorage
from system.storage import ImageStorage




# import os
# from uuid import uuid4
#
# def path_and_rename(path):
#     def wrapper(instance, filename):
#         ext = filename.split('.')[-1]
#         # get filename
#         if instance.pk:
#             filename = '{}.{}'.format(instance.pk, ext)
#         else:
#             # set filename as random string
#             filename = '{}.{}'.format(uuid4().hex, ext)
#         # return the whole path to the file
#         return os.path.join(path, filename)
#     return wrapper

# FileField(upload_to=path_and_rename('upload/here/'), ...)

# Create your models here.

class Users(models.Model):
    TYPE_CHOICES = (
        (0, '男'),
        (1, '女'),
        (2, '保密')
    )
    user_name = models.CharField(max_length=32, unique=True, db_index=True, verbose_name="用户名")
    user_email = models.EmailField(unique=True, db_index=True, verbose_name="邮箱")
    user_pwd = models.CharField(max_length=160, verbose_name="密码")
    user_idcard_num = models.CharField(max_length=32, unique=True, verbose_name="身份证号")
    user_avatar = models.ImageField(upload_to="static/upload/avatar", storage=ImageStorage(), null=True, verbose_name="头像")
    user_place = models.CharField(max_length=64, verbose_name="居住地", null=True)
    phonenum = models.CharField(max_length=12, verbose_name="手机号码", null=True)
    gender = models.IntegerField(default=2, help_text='请选择性别', verbose_name="性别", choices=TYPE_CHOICES)
    using_date = models.DateField(verbose_name="注册时间", null=True)
    isActive = models.BooleanField(default=False, verbose_name="激活")

    # 重写__str__,以便修改在后台的展示名称
    def __str__(self):
        return str(self.id)

    class Meta():
        # 1 重新定义表名:
        db_table = "users"
        # 2.
        verbose_name = "用户"
        # 3.
        verbose_name_plural = verbose_name


class Commodity(models.Model):
    commodity_name = models.CharField(max_length=80, db_index=True, verbose_name="商品名")
    commodity_discrib = models.TextField(max_length=500, verbose_name="商品描述", null=True)
    commodity_position = models.CharField(max_length=128, verbose_name="商品所在地")
    commodity_price = models.DecimalField(max_digits=7, decimal_places=2, verbose_name="商品价格")
    commodity_date = models.DateTimeField(verbose_name="上架时间")
    commodity_type = models.CharField(max_length=32, verbose_name="商品类型")
    commodity_count = models.IntegerField(verbose_name="商品数量")
    com_isactive = models.BooleanField(default=False, verbose_name="是否上架")
    com_isSold = models.BooleanField(default=False, verbose_name="是否卖出")
    # 一对多时,在多的实体中创建
    # 商品实体中增加了属性user, user_id
    # 在Users实体中增加了一个属性commodity_set(隐藏属性)
    # commodity_set表示的是当前的user对应的所有的数据的查询
    user = models.ForeignKey(Users)

    # 重写__str__,以便修改在后台的展示名称
    def __str__(self):
        return str(self.id)

    class Meta():
        # 1 重新定义表名:
        db_table = "commodity"
        # 2.
        verbose_name = "商品"
        # 3.
        verbose_name_plural = verbose_name


class Collection(models.Model):
    collection_date = models.DateTimeField(verbose_name="收藏时间")

    # 一对一的情况
    # 注:在Colletion表中会有一个users_id的列引用自Users表的主键
    #    Colletion实体类中会有一个user属性来表示对应的Users引用
    #    同时在user的实体中增加一个隐式属性collection
    user = models.OneToOneField(Users)

    # 多对多的情况:
    # 数据库中会创建第三张表collection_commodity 一个主键,两外键
    # Colletion实体类中会增加一个commodities属性来表示对应的Commodity引用
    # Commodity实体类中会增加一个collection_set属性来表示对应的Collection的查询引用
    commodities = models.ManyToManyField(Commodity)

    class Meta():
        # 1 重新定义表名:
        db_table = "collection"
        # 2.
        verbose_name = "收藏夹"
        # 3.
        verbose_name_plural = verbose_name


class Order(models.Model):
    order_count = models.IntegerField(verbose_name="订单商品数量")
    order_date = models.DateTimeField(verbose_name="订单时间")
    order_position = models.CharField(max_length=32, verbose_name="订单目的地")
    order_phone = models.CharField(max_length=12, verbose_name="收件人手机", null=True)
    order_user = models.CharField(max_length=16, verbose_name="收件人", null=True)
    order_sum = models.DecimalField(max_digits=7, decimal_places=2, verbose_name="订单金额",default=0)
    # 一对多时,在多的实体中创建
    # 订单实体中增加了属性user, user_id
    # 在Users实体中增加了一个属性order_set(隐藏属性)
    # order_set表示的是当前的user对应的所有的数据的查询
    user = models.ForeignKey(Users)
    commodity = models.ForeignKey(Commodity)

    # 重写__str__,以便修改在后台的展示名称
    def __str__(self):
        return str(self.commodity_id)

    class Meta():
        # 1 重新定义表名:
        db_table = "order"
        # 2.
        verbose_name = "订单"
        # 3.
        verbose_name_plural = verbose_name


class Photo(models.Model):
    photo = models.ImageField(upload_to="static/upload/picture", storage=ImageStorage(), verbose_name="商品照片")
    # 一对多时,在多的实体中创建
    # 订单实体中增加了属性commodity, commodity_id
    # 在Commodity实体中增加了一个属性photo_set(隐藏属性)
    # photo_set表示的是当前的Commodity对应的所有的数据的查询
    commodity = models.ForeignKey(Commodity)

    class Meta():
        # 1 重新定义表名:
        db_table = "photo"
        # 2.
        verbose_name = "商品照片"
        # 3.
        verbose_name_plural = verbose_name


class Order_feedback(models.Model):
    title = models.CharField(max_length=64,verbose_name="订单反馈的标题")
    content = models.TextField(verbose_name="订单反馈内容")
    feedback_date = models.DateTimeField(verbose_name="订单反馈日期")
    # 一对一的情况
    # 注:在Order_feedback表中会有一个order_id的列引用自Order表的主键
    #    Order_feedback实体类中会有一个order属性来表示对应的Order引用
    #    同时在order的实体中增加一个隐式属性order_feedback
    order = models.OneToOneField(Order)

    # 重写__str__,以便修改在后台的展示名称
    def __str__(self):
        return self.title

    class Meta():
        # 1 重新定义表名:
        db_table = "order_feedback"
        # 2.
        verbose_name = "订单反馈"
        # 3.
        verbose_name_plural = verbose_name

class Web_feedback(models.Model):
    problem = models.TextField(verbose_name="反馈的问题")
    feedback_date = models.DateTimeField(verbose_name="反馈日期")
    # 一对多时,在多的实体中创建
    # 订单实体中增加了属性user, user_id
    # 在Users实体中增加了一个属性Web_feedback_set(隐藏属性)
    # Web_feedback_set表示的是当前的user对应的所有的数据的查询
    user = models.ForeignKey(Users)

    def __str__(self):
        return str(self.id)

    class Meta():
        # 1 重新定义表名:
        db_table = "web_feedback"
        # 2.
        verbose_name = "网站反馈"
        # 3.
        verbose_name_plural = verbose_name


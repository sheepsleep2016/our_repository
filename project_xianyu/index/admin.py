from django.contrib import admin
from .models import *


# Register your models here.
class UsersAdmin(admin.ModelAdmin):
    # 1.定义能够在列表页显示的字段们
    #   取值为属性名组成的元组或列表
    list_display = ("id","user_name", "user_email", "user_idcard_num")
    # 2.定义能够在列表页链接到详情页的字段们
    #   取值必须在list_display中
    list_display_links = ("id","user_name", "user_email", "user_idcard_num",)
    # 4.定义在列表页右侧增加过滤器实现快速筛选
    #    取值为属性名组成的元组或列表
    list_filter = ("gender","using_date",)
    # 5.添加搜索字段
    #    取值为属性名组成的元组或列表
    search_fields = ("user_name", "user_email",)
    # 7.指定详情页的显示顺序
    # fields = ("name","email","age")
    # 8.详情页显示分组
    #    不能与field共存:
    # fieldsets = (
    # ("基本选项",{"fields":("name","age",)},),
    # ("高级选项",{"fields":("email","isActive",)},),
    # )


class CommodityAdmin(admin.ModelAdmin):
    list_display = ('id',"commodity_name", "commodity_position", "commodity_price", "commodity_type",'user_id')
    list_display_links = ('id',"commodity_name", "commodity_position", "commodity_type",'user_id')
    # 3.定义能够在列表页进行修改的字段
    #    取值必须在list_display中,但不能在list_display_links中
    list_editable = ("commodity_price",)
    # 4.定义在列表页右侧增加过滤器实现快速筛选
    #    取值为属性名组成的元组或列表
    list_filter = ("commodity_type","com_isactive","com_isSold",)
    # 5.添加搜索字段
    #    取值为属性名组成的元组或列表
    search_fields = ("commodity_position", "commodity_type", )
    # 6.指定日期分层器
    date_hierarchy = "commodity_date"


class OrderAdmin(admin.ModelAdmin):
    list_display = ("id","order_count", "order_date","order_position",)
    list_display_links = ("id","order_count",)
    # 3.定义能够在列表页进行修改的字段
    #    取值必须在list_display中,但不能在list_display_links中
    list_editable = ("order_date","order_position",)
    # 6.指定日期分层器
    date_hierarchy = "order_date"

class CollectionAdmin(admin.ModelAdmin):
    list_display = ("user_id","collection_date",)
    list_display_links = ("user_id","collection_date",)


class PhotoAdmin(admin.ModelAdmin):
    list_display = ('id',"photo", )
    list_display_links = ('id',"photo",)
    # 4.定义在列表页右侧增加过滤器实现快速筛选
    #    取值为属性名组成的元组或列表
    list_filter = ("commodity_id",)
    # 5.添加搜索字段
    #    取值为属性名组成的元组或列表
    search_fields = ("commodity_id",)


class Order_feedbackAdmin(admin.ModelAdmin):
    list_display = ("order_id","title", "feedback_date",)
    list_display_links = ("order_id","title",)
    list_editable = ("feedback_date",)

class Web_feedbackAdmin(admin.ModelAdmin):
    list_display = ("user_id","feedback_date",)
    list_display_links = ("user_id","feedback_date",)



# class PublisherAdmin(admin.ModelAdmin):
#     list_display = ("name", "address", "city")
#     # list_display_links = ()
#     list_editable = ("address", "city",)
#     list_filter = ("city","country",)
#     search_fields = ("name", "website",)
#     # fieldsets = (
#     #     ("基本选项", {"fields": ("name", "address","city",)},),
#     #     ("高级选项", {"fields": ("country", "website",)},),
#     # )


admin.site.register(Users, UsersAdmin)
admin.site.register(Commodity, CommodityAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(Collection, CollectionAdmin)
admin.site.register(Photo, PhotoAdmin)
admin.site.register(Web_feedback, Web_feedbackAdmin)
admin.site.register(Order_feedback, Order_feedbackAdmin)
# admin.site.register(Publisher,PublisherAdmin)

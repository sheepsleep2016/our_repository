from django.conf.urls import url

from . import views

urlpatterns = [

    # 网页输出 这是登录页面
    url(r'^login/$', views.login),
    url(r'^login00/$', views.login00),
    url(r'^loginout/$', views.loginout),
    # 网页输出 这是注册页面
    url(r'^register/$', views.register),
    # 网页输出 这是商品页面
    url(r'^(\d+)/$', views.shopping),
    url(r'^(\d+)/buying/$', views.buying),
    url(r'^paying/$', views.paying),
    url(r'^alipa/', views.alipaview),
    # url(r'^changelock/', views.changelock),
    # 网页输出 这是订单历史页面
    url(r'^order_list/$', views.order_list_history),
    # 网页输出 这是商品上架页面
    url(r'^putaway/(\d*)$', views.putaway),
    # 网页输出 这是个人信息页面
    url(r'^personal/(\w*)$', views.personal_info),
    # 网页输出 这是我的闲置页面
    url(r'^mythings/$', views.mythings),
    # 网页输出 这是忘记密码页面
    url(r'^update_pwd/$', views.update_pwd),
    # 网页输出 这是团队介绍页面
    url(r'^team/$', views.team_info),
    # 网页输出 这是网站介绍页面
    url(r'^about/$', views.about),
    # 网页输出 这是联系客服页面
    url(r'^connecting/$', views.service),
    url(r'^connecting/([1,2])/$', views.service00),
    url(r'^readme/$', views.readme),

    # 将从闲鱼获得数据导入到数据库中
    url(r'^get_data/$',views.get_data),
    # 获得验证码:
    url(r'^code/$',views.get_validate_code),
    # 实时对验证码进行验证:
    # url(r'^check_code/$', views.check_code),
    url(r'^upto/$',views.update_to),
    url(r'^upphoto/$', views.updatephoto),
    # url(r"^server/$",views.demo),
    url(r'^send000/$',views.send000),
    # url(r'^email_verify',views.email_verify),
    url(r'^checkUser/$', views.checkUser),

    # 主页
    url(r'^$', views.index),
    # 网页输出 这是主页分页面
    url(r'^([\u4e00-\u9fa5]+)/$', views.index00),

    url(r'^portal/sso', views.test_for_TVM),
]
import json
from datetime import datetime,date
from io import BytesIO
from uuid import uuid4
from django.core.mail import send_mail
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.core.files.base import ContentFile
from django.db.models import Count
from django.contrib.auth.hashers import make_password, check_password
from django.views.decorators.csrf import csrf_exempt,csrf_protect
from system import create_validate_code, read_excel
from system.updatephoto import *
from .models import *
import random,time
from .send_email import *
from app1.alipay.ailpay import AliPay
from project_xianyu.settings import ying_yong_si_yao, zhi_fu_bao_gong_yao
# Create your views here.

@csrf_exempt
def test_for_TVM(request,):
    if request.method == "POST":
        words = request.GET.get('method','')
        if words == 'isEnable':
            return HttpResponse(1)
        elif words == 'qryUserByTicket':
            response = """
<?xml version="1.0" encoding="UTF-8"?>
<response>
<head>
    <RESULT>8aeeef412f673d54012f8c726993013f</RESULT>
    <RESULT_MSG>门户系统</RESULT_MSG>
    <RESULT_MSGCODE>1000</RESULT_MSGCODE>
    <ACCOUNT>admin</ACCOUNT><!-- 门户名 -->
    <TICKET>123456789</TICKET>
</response>
"""
            return HttpResponse(response)
    return HttpResponse("zheshikongde")

# 网站首页
def index(request,):
    new = Commodity.objects.order_by("-commodity_date")
    # new = Commodity.objects.filter(id__lt=10)[1:10]
    list_com = []
    ii = 0
    for n in new:
        if (n.com_isactive and not n.com_isSold ) and ii<15:
            user = Users.objects.get(id=n.user_id)
            photo = Photo.objects.filter(commodity_id=n.id)
            photo_list =[]
            for p in photo:
                photo_list.append(p.photo)
            dict_new= {
                "commodity_name":n.commodity_name,
                "commodity_price":n.commodity_price,
                "id":"/"+str(n.id),
                "photo":photo_list,
                "user_name":user.user_name,
                "user_avatar":user.user_avatar
            }
            list_com.append(dict_new)
            ii +=1
    dict00 = check_cookie(request)
    dict00["list_com"] = list_com
    resp = render(request, "index.html",dict00)
    if not (dict00['key'] and dict00['msg'] ==0):
        resp.delete_cookie('user_name')
        resp.delete_cookie('user_pwd')
    return resp

# 主页的分页面
def index00(request, type):
    new = Commodity.objects.order_by("-commodity_date").filter(commodity_type=type)
    # new = Commodity.objects.filter(id__lt=10)[1:10]
    list_com = []
    # ii = 0
    for n in new:
        if (n.com_isactive and not n.com_isSold) :
            user = Users.objects.get(id=n.user_id)
            photo = Photo.objects.filter(commodity_id=n.id)
            photo_list = []
            for p in photo:
                photo_list.append("/"+str(p.photo))
            # print(type(photo_list[0]))
            dict_new = {
                "commodity_name": n.commodity_name,
                "commodity_price": n.commodity_price,
                "id": "/"+str(n.id),
                "photo": photo_list,
                "user_name": user.user_name,
                "user_avatar": "/"+str(user.user_avatar)
            }
            list_com.append(dict_new)
            # ii +=1
    dict00 = check_cookie(request)
    dict00["list_com"] = list_com
    resp = render(request, "index.html", dict00)
    if not (dict00['key'] and dict00['msg'] ==0):
        resp.delete_cookie('user_name')
        resp.delete_cookie('user_pwd')
    return resp

# 登录页面
def login(request):
    # if request.method == "post":

    return render(request, 'login.html')
# 登录处理程序
def login00(request):
    msg = request.POST.get('user_account')
    input_pwd = request.POST.get('user_pwd')
    rem = request.POST.get('rem')
    session_code = request.session.get('img')
    input_code = request.POST.get('code').upper()
    print(msg, input_pwd, input_code, session_code, rem)
    try:
        data = Users.objects.get(Q(user_email=msg) | Q(user_name=msg) | Q(phonenum=msg))
    except Exception as e:
        print(e)
    else:
        response = {'flag': False}
        if input_code != session_code:
            response["flag"] = '验证码错误'
            return HttpResponse(json.dumps(response))
        elif data and check_password(input_pwd,data.user_pwd):
            response["flag"] = 0
            resp = HttpResponse(json.dumps(response))
            if rem:
                resp.set_cookie("user_name", data.user_name, 60 * 60 * 24 * 30)
                resp.set_cookie("user_pwd", data.user_pwd, 60 * 60 * 24 * 30)
            else:
                resp.set_cookie("user_name", data.user_name, 60 * 30)
                resp.set_cookie("user_pwd", data.user_pwd, 60 * 30)
            return resp
        elif data:
            response["flag"] = '密码错误'
            return HttpResponse(json.dumps(response))
        else:
            response["flag"] = '您输入的帐号暂未注册，请您先进行注册'
            return HttpResponse(json.dumps(response))
# 退出登录页面
def loginout(request):
    resp=redirect("/login")
    resp.delete_cookie('user_name')
    resp.delete_cookie('user_pwd')
    return resp

# 注册界面
def register(request) :
    if request.method == 'GET':
        return render(request,'register.html')
    else :
        uname = request.POST.get('username')
        u_email = request.POST.get('email')
        uphone = request.POST.get('telphone')
        upwd = request.POST.get('password')
        m_upwd = make_password(upwd,None,'pbkdf2_sha256')  # 创建django密码，第三个参数为加密算法
        u_id = request.POST.get('identity')
        receive = Users.objects.values('user_name','user_email','phonenum','user_idcard_num')
        # print(receive)
        try :
            new_user = Users.objects.create()
            new_user.user_idcard_num = u_id
            new_user.user_name = uname
            new_user.user_pwd = m_upwd
            new_user.phonenum = uphone
            new_user.user_email = u_email
            new_user.isActive = True
            new_user.using_data = date.today()
            new_user.save()
        except :
            return HttpResponse('用户已存在')
        else:
            resp = redirect("/")
            resp.set_cookie("user_name", uname, 60 * 30)
            resp.set_cookie("user_pwd", m_upwd, 60 * 30)
            return resp

def checkUser(request) :
    if request.is_ajax() :
        data = request.POST
        datanum = request.POST.get('num')
        receive = Users.objects.filter(Q(phonenum=datanum) | Q(user_name=datanum) |
                                       Q(user_email=datanum) | Q(user_idcard_num=datanum))
        response = {'flag':False}
        if receive :
            response["flag"] = 0
            print('111')
        else :
            response["flag"] = 1
        return HttpResponse(json.dumps(response))

def send000(request) :
    email = request.POST.get('email')
    print(email)
    code = send_register_email(email)
    response = {'flag': code}
    return HttpResponse(json.dumps(response))

def readme(request):
    return render(request,"readme.html")
"""
# def check_code(request):
#     session_code = request.session.get('img')
#     input_code = request.GET.get('code').upper()
#     print(input_code,session_code)
#     if input_code != session_code:
#         return HttpResponse("true")
#     return

# 注册页面
# def register(request):
#     if request.method == 'POST':
#         if request.session.get('img') == request.POST.get('img').upper():
#             return 'OK'
#         return 'Error'
#     return render(request, "register.html")
#     return HttpResponse("这是注册页面")
"""

# 个人信息界面
def personal_info(request,word):
    if word == "changepwd":
        dict_check = check_cookie(request)
        if dict_check['key']:
            if request.method == "POST":
                user_name = dict_check['user_name']
                pwd_old = request.POST.get("pwd_old")
                pwd_new = request.POST.get("pwd_new")
                if check_password(pwd_old, dict_check['user_pwd']):  # 返回的是一个bool类型的值，验证密码正确与否
                    obj = Users.objects.get(user_name=user_name)
                    obj.user_pwd = make_password(pwd_new,None,'pbkdf2_sha256')
                    obj.save()
                    response = {"msg":  0}
                    resp = HttpResponse(json.dumps(response))
                    resp.set_cookie("user_name", user_name, 60 * 60 * 24 * 30)
                    resp.set_cookie("user_pwd", pwd_new, 60 * 60 * 24 * 30)
                    return resp
                else:
                    response = {"msg": '原始密码错误'}
                    return HttpResponse(json.dumps(response))
            return render(request, "p_changepwd.html", dict_check)
        elif not (dict_check['key'] and dict_check['msg'] ==0):
            resp = redirect("/login")
            resp.delete_cookie('user_name')
            resp.delete_cookie('user_pwd')
            return resp
        else:
            return redirect("/login")
    else:
        dict_check = check_cookie(request)
        if dict_check['key']:
            if request.method == "GET":
                user = Users.objects.get(user_name = dict_check["user_name"])
                dict_check["user_email"] = user.user_email
                dict_check["user_avatar"] = "/"+str(user.user_avatar)
                dict_check["user_palce"] = user.user_place
                strii = user.user_idcard_num[6:14]
                dict_check["birth"] = datetime.strptime(strii,"%Y%m%d").strftime('%Y-%m-%d')
                dict_check["user_place"] = user.user_place
                dict_check["phonenum"] = user.phonenum
                dict_check["gender"] = user.gender
                dict_check["using_date"] = user.using_date
                return render(request, "personal_info.html",dict_check)
            else:
                gender = request.POST.get("gender")
                province = request.POST.get("province")
                city = request.POST.get("city")
                avatar = request.FILES.get("files")
                user = Users.objects.get(user_name=dict_check["user_name"])
                print(gender,province,city,user,avatar)
                if province:
                    user.user_place = province+"/"+city
                if avatar:
                    file_content = ContentFile(avatar.read())
                    user.user_avatar.save(avatar.name, file_content)
                user.gender = gender
                user.save()
                return redirect("/personal")
        elif not (dict_check['key'] and dict_check['msg'] == 0):
            resp = redirect("/login")
            resp.delete_cookie('user_name')
            resp.delete_cookie('user_pwd')
            return resp
        else:
            return redirect("/login")
    # return HttpResponse("这是个人信息页面")

# 我的闲置
def mythings(request):
    dict_check = check_cookie(request)
    if dict_check['key']:
        if request.method == "GET":
            user = Users.objects.get(user_name=dict_check["user_name"])
            list_order = []
            print(user.commodity_set.all())
            for comm in user.commodity_set.all():
                dict_comm = {}
                photo = Photo.objects.filter(commodity_id=comm.id)
                dict_comm["id"] = comm.id
                dict_comm["date"] = comm.commodity_date
                dict_comm["count"] = comm.commodity_count
                dict_comm["position_send"] = comm.commodity_position
                dict_comm["type"] = comm.commodity_type
                dict_comm["photo"] = "/" + str(photo[0].photo)
                dict_comm["name"] = comm.commodity_name
                dict_comm["price"] = comm.commodity_price
                dict_comm["totalprice"] = comm.commodity_price * comm.commodity_count
                isactive = ""
                issold = ""
                if comm.com_isactive:
                    isactive = "已上架"
                else:
                    isactive = "未上架"
                if comm.com_isSold:
                    issold = "已卖出"
                else:
                    issold = "未卖出"
                dict_comm["isactive"] = isactive
                dict_comm["issold"] = issold
                list_order.append(dict_comm)
            dict_check["list_order"] = list_order
            print(list_order)
            return render(request, "p_mythings.html", dict_check)
    elif not (dict_check['key'] and dict_check['msg'] == 0):
        resp = redirect("/login")
        resp.delete_cookie('user_name')
        resp.delete_cookie('user_pwd')
        return resp
    else:
        return redirect("/login")

# 修改密码页面
def update_pwd(request):
    if request.method == 'POST':
        msg = request.POST.get("msg")
        response = {'flag': False}
        if msg == '0':
            account = request.POST.get("user_account")
            try:
                data = Users.objects.get(Q(user_email=account)|Q(user_name=account)|Q(phonenum=account))
            except Exception as e:
                response["flag"] = 0
                return HttpResponse(json.dumps(response))
            else:
                # send_mail的参数分别是  邮件标题，邮件内容，发件箱(settings.py中设置过的那个)，
                # 收件箱列表(可以发送给多个人),失败静默(若发送失败，报错提示我们)
                # if data:
                    email = data.user_email
                    valicate_code = uuid4().hex
                    send_mail('欢乐GO网站修改密码的验证邮件', """亲爱的用户您好!:
    此邮件用于修改密码的验证,以保证您的帐号安全,请复制以下验证码在修改密码界面进行邮箱验证:
    %s
    注:若该邮件接收人不是本人,请忽略本邮件或删除;给您造成的不便请谅解!""" % valicate_code, 'sheepsleep2016@163.com',
    [email], fail_silently=False)
                    response["flag"] = valicate_code
                    return HttpResponse(json.dumps(response))
                # else:
                #     print("123456789")
                #     response["flag"] = 0
                #     return HttpResponse(json.dumps(response))
        elif msg == '1':
            new_pwd = request.POST.get("new_pwd")
            account = request.POST.get("user_account")
            data = Users.objects.get(Q(user_email=account) | Q(user_name=account) | Q(phonenum=account))
            data.user_pwd = make_password(new_pwd,None,'pbkdf2_sha256')
            data.save()
            response["flag"] = "修改密码成功!"
            return HttpResponse(json.dumps(response))
    return render(request, "p_reset_password.html")
    # return HttpResponse("这是修改密码页面")

# 历史订单页面
def order_list_history(request):
    dict_check = check_cookie(request)
    if dict_check['key']:
        user_name = request.COOKIES["user_name"]
        user = Users.objects.get(user_name=user_name)
        # 得到对应的所有order对象的属性字典的列表
        orders = user.order_set.all()
        # 创建commodity的对象列表
        list_order = []
        for order in orders:
            dict_comm = {}
            comm = Commodity.objects.get(id=order.commodity_id)
            photo = Photo.objects.filter(commodity_id=order.commodity_id)
            user_sold = Users.objects.get(id=comm.user_id)
            photo_list = []
            print(photo, comm)
            for p in photo:
                photo_list.append("/"+str(p.photo))
            dict_comm["id"] = order.id
            dict_comm["date"] = order.order_date
            dict_comm["count"] = order.order_count
            dict_comm["position_recv"] = order.order_position
            dict_comm["position_send"] = comm.commodity_position
            dict_comm["photo"] = photo_list
            dict_comm["name"] = comm.commodity_name
            dict_comm["price"] = comm.commodity_price
            dict_comm["totalprice"] = comm.commodity_price*order.order_count
            dict_comm["solder_name"] = user_sold.user_name
            dict_comm["solder_phone"] = user_sold.phonenum
            list_order.append(dict_comm)
        dict_check["list_order"]=list_order
        return render(request, "p_list_order.html", dict_check)
    elif not (dict_check['key'] and dict_check['msg'] == 0):
        resp = redirect("/login")
        resp.delete_cookie('user_name')
        resp.delete_cookie('user_pwd')
        return resp
    else:
        return redirect("/login")
    # return HttpResponse("这是订单历史页面")

# 商品页
def shopping(request, com_id):
    comm = Commodity.objects.get(id=com_id)
    if not comm.com_isSold and comm.com_isactive:
        count = 0
        dict00 = check_cookie(request)
        user = Users.objects.get(id=comm.user_id)
        photo = Photo.objects.filter(commodity_id=comm.id)
        photo_list =[]
        print(str(photo[0].photo),comm,user)
        for p in photo:
            path00 = str(p.photo)
            photo_list.append("/"+path00.split("/")[-1])
        path01 = str(photo[0].photo)
        path_photo = "/"+"/".join(path01.split("/")[0:-1])
        comms = user.commodity_set.all()
        for comm00 in comms:
            if Order.objects.filter(commodity_id=comm00.id):
                count += 1
        dict_shopping = {
            "commodity_name": comm.commodity_name,
            "commodity_price": comm.commodity_price,
            "commodity_position": comm.commodity_position,
            "commodity_discrib": comm.commodity_discrib,
            "commodity_date": comm.commodity_date,
            "commodity_count": comm.commodity_count,
            "photo":photo_list,
            "user_name":user.user_name,
            "user_avatar":"/"+str(user.user_avatar),
            "useingdate":user.using_date,
            "phonenum":user.phonenum,
            "gender":user.gender,
            "order_count":count,
            "path_photo":path_photo,
            "full_path":"/"+str(photo[0].photo),
            "dict00":dict00,
        }
        # comm.com_isactive=True
        # comm.save()
        list_msg = [photo_list,path_photo,]
        dict_shopping["list_comm"] = json.dumps(list_msg)
        return render(request, "b_shopping.html", dict_shopping)
    else:
        HttpResponse("该商品不存在！")
     # return HttpResponse("这是商品页面")

# 下单页
def buying(request,com_id):
    dict_check = check_cookie(request)
    # if dict_check['key']:
    if request.method == "POST":
        user_name = request.COOKIES["user_name"]
        comm = Commodity.objects.get(id=com_id)

        dict_comm = {
            "user_id": Users.objects.get(user_name=user_name).id,
            "commodity_name": comm.commodity_name,
            "commodity_discrib": request.POST.get('comm_discrib'),
            "commodity_position": request.POST.get('comm_position'),
            "commodity_price": request.POST.get('comm_price'),
            "commodity_date": datetime.now(),
            "commodity_type": request.POST.get('type'),
            "commodity_count": request.POST.get('count'),
            "com_isactive": request.POST.get('isactive')
        }
        try:
            obj = Commodity(**dict_comm)
            obj.save()
        except:
            response = {"flag":'false'}
            return HttpResponse(json.dumps(response))
        else:
            response = {"flag": 0}
            return HttpResponse(json.dumps(response))
    else:
        user_name = request.COOKIES["user_name"]
        comm = Commodity.objects.get(id=com_id)
        photo = Photo.objects.filter(commodity_id=com_id)
        user_sold = Users.objects.get(id=comm.user_id)
        photo_list = []
        print(photo, comm)
        for p in photo:
            photo_list.append("/" + str(p.photo))
        dict_comm={
            "id":comm.id,
            "comm_name":comm.commodity_name,
            "comm_position":comm.commodity_position,
            "comm_price":comm.commodity_price,
            "count":comm.commodity_count,
            "photo":photo_list[0],
            "dict_check":dict_check,
        }
        # comm.com_isactive = False
        # comm.save()
        return render(request, "b_buying.html", dict_comm)

# 付款界面
def paying(request):
    if request.method == "POST":
        user = Users.objects.get(user_name=request.COOKIES["user_name"])
        province = request.POST.get("province")
        city = request.POST.get("city")
        position = request.POST.get("position")
        order_position = "/".join([province,city,position])
        order_user = request.POST.get("order_user")
        order_phone = request.POST.get("phone")
        comm_id = int(request.POST.get("comid"))
        count = int(request.POST.get("count"))

        order_sum = float(request.POST.get("price"))
        print(request.POST.get("price"), order_position,order_user,order_phone,comm_id,count)
        order_date = datetime.now()
        fn = time.strftime('%Y%m%d%H%M%S')
        order_id = fn +'%d_%d' % (random.randint(0, 100),comm_id)
        comm = Commodity.objects.get(id = comm_id)
        """支付请求过程"""
        # 传递参数初始化支付类
        alipay = AliPay(
            appid="2016092900622750",  # 设置签约的appid
            app_notify_url="http://projectsedus.com/",  # 异步支付通知url
            app_private_key_path=ying_yong_si_yao,  # 设置应用私钥
            alipay_public_key_path=zhi_fu_bao_gong_yao,  # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
            debug=True,  # 默认False,                                   # 设置是否是沙箱环境，True是沙箱环境
            return_url="http://127.0.0.0:8000/alipa/"  # 同步支付通知url
        )

        # 传递参数执行支付类里的direct_pay方法，返回签名后的支付参数，
        url = alipay.direct_pay(
            subject=comm.commodity_name,  # 订单名称
            # 订单号生成，一般是当前时间(精确到秒)+用户ID+随机数
            out_trade_no=order_id,  # 订单号
            total_amount=order_sum,  # 支付金额
            return_url="http://127.0.0.0:8000/alipa/"  # 支付成功后，跳转url
        )

        # 将前面后的支付参数，拼接到支付网关
        # 注意：下面支付网关是沙箱环境，
        re_url = "https://openapi.alipaydev.com/gateway.do?{data}".format(data=url)
        print(re_url)
        # 最终进行签名后组合成支付宝的url请求

        # 将数据导入到order表中
        dict_order = {
            "order_count":count,
            "order_date":order_date,
            "order_position":order_position,
            "order_phone":order_phone,
            "order_user":order_user,
            "order_sum":order_sum,
            "user_id":user.id,
            "commodity_id":comm_id,
        }
        ord = Order(**dict_order)
        ord.save()

        response = {"flag":False}
        # 商品相关信息更新：
        if count == comm.commodity_count:
            comm.com_isactive = False
            comm.com_isSold = True
            comm.save()
            response["flag"] = re_url
        elif comm.com_isSold == True:
            response["flag"] = 0
        else:
            comm.com_isSold = True
            comm.commodity_count = comm.commodity_count - count
            comm.save()
            response["flag"] = re_url
        return HttpResponse(json.dumps(response))
        # response = {"msg": '原始密码错误'}
        # return HttpResponse(json.dumps(response))

"""
# def changelock(request):
#     if request.method == "POST":
#         id00 = request.POST.get("comid")
#         print(id00)
#         comm = Commodity.objects.get(id = id00)
#         comm.com_isactive = True
#         comm.save()
#         response = {"flag": 0}
#         return HttpResponse(json.dumps(response))
"""
# 商品上架页
def putaway(request,comm_id):
    dict_check = check_cookie(request)
    if dict_check['key']:
        if request.method == "POST":
            user_name = request.COOKIES["user_name"]
            imgs = request.FILES.getlist("i")
            comm_date = datetime.now()
            user_id = Users.objects.get(user_name=user_name).id

            dict_comm = {
                "user_id" : user_id,
                "commodity_name": request.POST.get('comm_name'),
                "commodity_discrib":  request.POST.get('comm_discrib'),
                "commodity_position" : request.POST.get('comm_province')+request.POST.get('comm_city'),
                "commodity_price" : request.POST.get('comm_price'),
                "commodity_date"  :comm_date,
                "commodity_type"  :request.POST.get('comm_type'),
                "commodity_count" : request.POST.get('comm_count'),
                "com_isactive" :  bool(request.POST.get('isactive')),
            }
            print(dict_comm)
            try:
                # pass
                obj = Commodity(**dict_comm)
                obj.save()
            except :
                response = {"flag": 'false'}
                return HttpResponse(json.dumps(response))
            else:
                for img in imgs:
                    obj01 = Photo()
                    obj01.commodity_id = \
                        Commodity.objects.get(commodity_date=comm_date,user_id=user_id).id
                    content = bytes()
                    # print(img.chunks())
                    for chunk in img.chunks():
                        content += chunk
                    file_content = ContentFile(content)
                    # print(content[1:100])
                    obj01.photo.save(img.name, file_content)
                    obj01.save()
                response = {"flag": 0}
                return HttpResponse(json.dumps(response))
        else:
            if comm_id:
                comm = Commodity.objects.get(id = comm_id)
                dict_check["comm_name"] = comm.commodity_name
                dict_check["comm_discrib"] = comm.commodity_discrib
                dict_check["comm_price"] = comm.commodity_price
                dict_check["comm_name"] = comm.commodity_name
                dict_check["comm_name"] = comm.commodity_name
            return render(request, "b_putaway.html", dict_check)
    elif dict_check['msg'] == 0:
        resp = redirect("/login")
        resp.delete_cookie('user_name')
        resp.delete_cookie('user_pwd')
        return resp
    else:
        return redirect("/login")

# 商品收藏页(时间限制，取消)
# def collection(request):
    # return render(request, "collection.html")
    # return HttpResponse("这是商品收藏页")

# 关于网站页
def about(request):
    dict00 = check_cookie(request)
    resp = render(request, "s_about.html", dict00)
    if dict00['key'] is False and dict00['msg'] == 0:
        resp.delete_cookie('user_name')
        resp.delete_cookie('user_pwd')
        return resp
    return resp
    # return HttpResponse("这是关于网站页面")

# 制作团队页
def team_info(request):
    dict00 = check_cookie(request)
    resp = render(request, "s_team_info.html", dict00)
    if dict00['key'] is False and dict00['msg'] == 0:
        resp.delete_cookie('user_name')
        resp.delete_cookie('user_pwd')
        return resp
    return resp
    # return HttpResponse("这是制作团队页")

# 联系客服页
def service(request):
    dict00 = check_cookie(request)
    resp = render(request, "S_service.html", dict00)
    if dict00['key'] is False and dict00['msg'] == 0:
        resp.delete_cookie('user_name')
        resp.delete_cookie('user_pwd')
        return resp
    return resp

# 联系客服反馈页面
def service00(request, word):
    user_name = request.COOKIES["user_name"]
    user = Users.objects.get(user_name=user_name)
    if word == '1':
        orders = user.order_set.all()
        list_order = []
        for order in orders:
            comm = Commodity.objects.get(id=order.commodity_id)
            dict00 = {
                "order_id": order.id,
                "order_date": order.order_date,
                "comm_name": comm.commodity_name,
            }
            list_order.append(dict00)
        if request.method == "POST":
            title = request.POST.get("title")
            content = request.POST.get("content")
            order_id = request.POST.get("order_id")
            date = datetime.now()
            dict00={
                "title":title,
                "content":content,
                "order_id":order_id,
                "feedback_date":date,
            }
            obj = Order_feedback(**dict00)
            obj.save()
            response={"flag":0}
            return HttpResponse(json.dumps(response))
        return render(request, "S_order_feedback.html", {"list_order":list_order})
    elif word == '2':
        if request.method == "POST":
            content = request.POST.get("content")
            order_id = user.id
            date = datetime.now()
            dict00 = {
                "problem": content,
                "order_id": order_id,
                "feedback_date": date,
            }
            obj = Order_feedback(**dict00)
            obj.save()
            return redirect("/")
        return render(request, "S_web_feedback.html")
    # return HttpResponse("这是联系客服页")

def get_validate_code(request):
    # 把strs发给前端,或者在后台使用session保存
    code_img, strs = create_validate_code.create_validate_code()
    buf = BytesIO()
    code_img.save(buf, 'jpeg')
    request.session['img'] = strs.upper()
    # ['Content-Type'] = 'image/gif'
    return HttpResponse(buf.getvalue(), content_type='image/gif')

# 将闲鱼上的数据导入到数据库
def get_data(request):
    # 服装类的信息已经导入了
    data_path = "/home/tarena/虚拟用户 - 副本.xls"

    # data_path = None
    get_data= read_excel.ExcelData(data_path, sheetname='Sheet5')
    list_user,list_comm = get_data.readExcel()
    for dictuser in list_user:
        obj = Users(**dictuser)
        obj.save()

    for dictcom in list_comm:
        obj = Commodity(**dictcom)
        obj.save()

    return HttpResponse("增加数据成功!!")


# 对数据进行修改
def update_to(request):
    # # user = Users.objects.get(user_name="linlin")
    # userlist =Users.objects.all()
    # value = [date(2019, 5, 11),date(2019, 4, 11),date(2019, 5, 11),
    #          date(2019, 4, 9),date(2019, 5, 18),date(2019, 5, 11),
    #          date(2019, 5, 13),date(2019, 5, 11),date(2019, 4, 30),
    #          date(2019, 5, 14),date(2019, 5, 17),date(2019, 5, 10)]
    # # value_place = ["湖北省/黄冈市","湖北省/黄石市","湖北省/荆州市","湖北省/武汉市","湖北省/鄂州市","河南省/信阳市",
    # #                "上海市/浦东区","广东省/广州市","湖南省/衡阳市","广东省/深圳市","广西省/北海市","重庆市/渝北区"]
    # for us in userlist:
    #     print(us.using_date)
    #     if not us.using_date:
    #         print("00000")
    #         us.using_date =random.choice(value)
    #     # if not us.user_place:
    #     #     us.user_place = random.choice(value_place)
    #     us.save()
    # return HttpResponse("修改成功")
    # # obj = Commodity.objects.get(id=46)
    # # obj.commoduty_date = datetime(2019, 5, 11, 16, 10)
    # # obj.save()

    comms = Commodity.objects.all()
    for com in comms:
        if not com.com_isactive and not com.com_isSold:
            com.com_isactive = True
            com.save()
    return HttpResponse("修改成功")

"""
# 上传的图片传入数据库
# def save_file(request):
#     mymodel = MyModel.objects.get(id=1)
#     # 读取上传的文件中的video项为二进制文件
#     file_content = ContentFile(request.FILES['video'].read())
#     # ImageField的save方法，第一个参数是保存的文件名，第二个参数是ContentFile对象，里面的内容是要上传的图片、视频的二进制内容
#     mymodel.video.save(request.FILES['video'].name, file_content)

# with open("/home/tarena/1902/project_xianyu/static/image/三国演义.jpg","rb") as file:
#     obj01 = Photo.objects.get(commodity_id=1)
#     file_content = ContentFile(file.read())
#     obj01.photo.save("A.jpg",file_content)
# return HttpResponse("修改成功")


# send_mail的参数分别是  邮件标题，邮件内容，发件箱(settings.py中设置过的那个)，
# 收件箱列表(可以发送给多个人),失败静默(若发送失败，报错提示我们)
# send_mail('Subject here', 'Here is the message.', 'sheepsleep@163.com',
#     ['to@example.com'], fail_silently=False)

# GET的示例
# def demo(request):
#     uname = request.GET["uname"]
#     uage = request.GET["uage"]
#     return HttpResponse("姓名:%s;/n年龄:%s"%(uname,uage))
"""

# 将照片导入到数据库中
def updatephoto(request):
    filenames = '/home/tarena/xianyu_tupian/运动'
    getdata = pppp(filenames)
    list_photo = getdata.get_photo0000()
    # for i in list_photo:
    #     print(i)
    for p in list_photo:
        with open(p["full_path"], "rb") as file:
            obj01 = Photo()
            obj01.commodity_id =p["commodity_id"]
            file_content = ContentFile(file.read())
            obj01.photo.save(p["file_name"],file_content)
            obj01.save()
    return HttpResponse("增加图片成功")

# 核对是否有cookie
def check_cookie(request):
    dict00 = {"key": False, "user_name": None, 'msg': 0}
    try:
        request.COOKIES["user_name"]
    except:
        dict00["msg"] = 1
    else:
        user_name = request.COOKIES["user_name"]
        user_pwd = request.COOKIES["user_pwd"]
        if Users.objects.filter(user_name=user_name, user_pwd=user_pwd):
            dict00["key"] = True
            dict00["user_name"] = user_name
            dict00["user_pwd"] = user_pwd
            print("获取了cookies")
    return dict00

# def checkUser(request) :
#     if request.is_ajax() :
#         data = request.POST
#         datanum = request.POST.get('num')
#         receive = Users.objects.filter(Q(phonenum=datanum) | Q(user_name=datanum) | Q(user_email=datanum) | Q(user_idcard_num=datanum))
#     # uphone = request.GET.get('uphone')
#     # uuser = request.GET.get('uuser')
#     # uemail = request.GET.get('uemail')
#     # ucard = request.GET.get('ucard')
#     # receive = Users.objects.filter(Q(phonenum=uphone) | Q(user_name=uuser) | Q(user_email=uemail) | Q(user_idcard_num=ucard))
#         print(receive)
#         response = {'flag':False}
#         if receive :
#             response["flag"] = 0
#         else :
#             response["flag"] = 1
#         return HttpResponse(json.dumps(response))

# django 加密算法
def check_pwd(pwd, ):
    pwd='4562154'
    mpwd=make_password(pwd,None,'pbkdf2_sha256')  # 创建django密码，第三个参数为加密算法
    pwd_bool=check_password(pwd,mpwd)# 返回的是一个bool类型的值，验证密码正确与否

@csrf_exempt
def alipaview(request):
    if request.method == "GET":
        processed_dict = {}  # 接收支付宝传递参数
        for key, value in request.GET.items():  # 循环参数
            processed_dict[key] = value  # 将参数添加到字典
        sign = processed_dict.pop('sign', None)  # 单独拿出sign字段

        # 传递参数初始化支付类
        alipay = AliPay(
            appid="2016092900622750",  # 设置签约的appid
            app_notify_url="http://47.52.39.160:8000/alipa/",  # 异步支付通知url
            app_private_key_path=ying_yong_si_yao,  # 设置应用私钥
            alipay_public_key_path=zhi_fu_bao_gong_yao,  # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
            debug=True,  # 默认False,                                   # 设置是否是沙箱环境，True是沙箱环境
            return_url="http://47.52.39.160:8000/alipa/"  # 同步支付通知url，跳转地址
        )

        # 验证支付宝返回的合法性
        yan_zhen = alipay.verify(processed_dict, sign)
        if yan_zhen is True:  # 判断如果合法
            out_trade_no = processed_dict.get('out_trade_no', None)  # 商户订单号
            trade_no = processed_dict.get('trade_no', None)  # 支付宝交易号
            buyer_id = processed_dict.get('buyer_id', None)  # 买家支付宝用户号
            trade_status = processed_dict.get('trade_status', None)  # 交易状态
            total_amount = processed_dict.get('total_amount', None)  # 订单金额
            receipt_amount = processed_dict.get('receipt_amount', None)  # 实收金额
            subject = processed_dict.get('subject', None)  # 订单标题
            gmt_payment = processed_dict.get('gmt_payment', None)  # 交易付款时间

            # 数据库操作
            print(out_trade_no)
            print(trade_no)
            print(buyer_id)
            print(trade_status)
            print(total_amount)
            print(receipt_amount)
            print(subject)
            print(gmt_payment)

            # 向支付宝返回success，告诉他我们已经处理，不然他会不停的通知
            return HttpResponse('success')

    if request.method == "POST":                        # post请求支付宝异步通知
        processed_dict = {}                             # 接收支付宝传递参数
        for key, value in request.POST.items():         # 循环参数
            processed_dict[key] = value                 # 将参数添加到字典
        sign = processed_dict.pop('sign', None)         # 单独拿出sign字段

        # 传递参数初始化支付类
        alipay = AliPay(
            appid="2016092900622750",                                   # 设置签约的appid
            app_notify_url="http://47.52.39.160:8000/alipa/",           # 异步支付通知url
            app_private_key_path=ying_yong_si_yao,  # 设置应用私钥
            alipay_public_key_path=zhi_fu_bao_gong_yao,  # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
            debug=True,  # 默认False,                                   # 设置是否是沙箱环境，True是沙箱环境
            return_url="http://47.52.39.160:8000/alipa/"                # 同步支付通知url
        )

        # 验证支付宝返回的合法性
        yan_zhen = alipay.verify(processed_dict, sign)
        if yan_zhen is True:                                                # 判断如果合法
            out_trade_no = processed_dict.get('out_trade_no', None)         # 商户订单号
            trade_no = processed_dict.get('trade_no', None)                 # 支付宝交易号
            buyer_id = processed_dict.get('buyer_id', None)                 # 买家支付宝用户号
            trade_status = processed_dict.get('trade_status', None)         # 交易状态
            total_amount = processed_dict.get('total_amount', None)         # 订单金额
            receipt_amount = processed_dict.get('receipt_amount', None)     # 实收金额
            subject = processed_dict.get('subject', None)                   # 订单标题
            gmt_payment = processed_dict.get('gmt_payment', None)           # 交易付款时间

            # 数据库操作
            print(out_trade_no)
            print(trade_no)
            print(buyer_id)
            print(trade_status)
            print(total_amount)
            print(receipt_amount)
            print(subject)
            print(gmt_payment)

            # 向支付宝返回success，告诉他我们已经处理，不然他会不停的通知
            return HttpResponse('success')

# """支付请求过程"""
# # 传递参数初始化支付类
# alipay = AliPay(
#     appid="2016092900622750",  # 设置签约的appid
#     app_notify_url="http://projectsedus.com/",  # 异步支付通知url
#     app_private_key_path=u"ying_yong_si_yao.txt",  # 设置应用私钥
#     alipay_public_key_path="zhi_fu_bao_gong_yao.txt",  # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
#     debug=True,  # 默认False,                                   # 设置是否是沙箱环境，True是沙箱环境
#     return_url="http://47.92.87.172:8000/"  # 同步支付通知url
# )
#
# # 传递参数执行支付类里的direct_pay方法，返回签名后的支付参数，
# url = alipay.direct_pay(
#     subject="测试订单",  # 订单名称
#     # 订单号生成，一般是当前时间(精确到秒)+用户ID+随机数
#     out_trade_no="201702021225",  # 订单号
#     total_amount=100,  # 支付金额
#     return_url="http://47.92.87.172:8000/"  # 支付成功后，跳转url
# )
#
# # 将前面后的支付参数，拼接到支付网关
# # 注意：下面支付网关是沙箱环境，
# re_url = "https://openapi.alipaydev.com/gateway.do?{data}".format(data=url)
# print(re_url)
# # 最终进行签名后组合成支付宝的url请求
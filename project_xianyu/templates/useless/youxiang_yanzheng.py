str.pk
import re

class RegisterView(View):
    def post(self,request):
        user_name = request.POST.get('username')
        password = request.POST.get('password')
        cpassword = request.POST.get('cpassword')
        email = request.POST.get('email')
        '''判断数据是否为空'''
        if not all([user_name, password, cpassword, email]):
            return render(request, 'index.html')

        if not re.match(r'^([a-zA-Z0-9_-])+@([a-zA-Z0-9_-])+((\.[a-zA-Z0-9_-]{2,3}){1,2})$', email):
            return render(request, 'index.html', {'errmsg': '邮箱不符合规范'})

        

        '''判断重复的操作'''
        '''判断邮箱'''
        try:
            user = UserInfo.objects.filter(email__exact=email)

        except Exception as e:
            user = None

        if user:
            return render(request, 'index.html', {'errmsg': '邮箱已经被使用'})

        '''判断用户名'''
        try:
            usern = UserInfo.objects.get(username=user_name)

        except Exception as e:
            usern = None

        if usern:
            return render(request, 'index.html', {'errmsg': '用户名已经被使用'})

        '''创建一个用户对象'''
        user = UserInfo.objects.create_user(username=user_name, password=password, email=email)
  

      '''将激活标志设置为0'''
        user.is_active = 0
        user.save()

        t = tr(settings.SECRET_KEY,3600)
        user_id_dict = {'user_id':user.id}
        active_id = t.dumps(user_id_dict)
        active_id = active_id.decode()
        print(active_id)

      
        send_email_celery(to_email=email, active_id=active_id)
        subject = '项目名'
        message = '<div><a href="http://127.0.0.1:8000/user/register">这是激活邮件</a></div>'
        from_email = '发送邮箱的地址'
        recipient_list = [email]
        html_message = '<div><a href="http://127.0.0.1:8000/user/active/%s">这是激活邮件</a></div>'%active_id
        send_mail(subject=subject,message=message,from_email=from_email,recipient_list=recipient_list,html_message=html_message)
	return HttpResponse('激活邮件')

class ActiveHandler(View):
    def get(self,request,obj):
      
        t = tr(settings.SECRET_KEY, 3600)
        print(obj)
        try:
            user_id = t.loads(obj)
            userid = user_id['user_id']
            user = UserInfo.objects.get(id = userid)
            user.is_active = 1
            user.save()
            return HttpResponse('激活成功')
        except Exception as e:
            return HttpResponse('激活失败')

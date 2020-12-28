import random
import string
from django.core.mail import send_mail
# from .models import EmailVerify



def random_str(randomlenth=8):
    str_all = string.ascii_letters+string.digits
    send_str = random.sample(str_all, randomlenth)
    send_str= "".join(send_str)
    return send_str

def send_register_email(email, send_type = "register"):
    # send_type = "register"

    code = random_str()

    # print(code)
    # EmailVerify.code = code
    # # email_record.code = code
    # EmailVerify.email = email
    # EmailVerify.send_type = send_type
    email_title = "欢乐GO邮箱验证"
    email_body  = "请完成验证"
    if 1 :
        email_body = "激活码:%s,\n请完成验证"%(code)
        send_status = send_mail(email_title, email_body, 'sheepsleep2016@163.com', [email,], )
        return code

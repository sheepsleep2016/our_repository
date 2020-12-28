from django.http import HttpResponse
from django.shortcuts import render

def login(request):
    return HttpResponse("这是登录页面")

def register(request):
    return HttpResponse("这是注册页面")
from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth import login as _login
from django.contrib.auth import logout as _logout
from rest_framework.response import Response
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_http_methods
from rest_framework.decorators import api_view
import json

# Create your views here.


@api_view(['POST'])
def login(request):
    response = {}
    if request.method == 'POST':
        # postBody = request.body
        # json_result = json.loads(postBody)
        # # print(json_result['username'])

        username = request.POST.get('username')
        password = request.POST.get('password')
        print(username, password)
        user = User.objects.filter(username=username).first()
        if not username:
            response['msg'] = '请输入用户名'
        elif not password:
            response['msg'] = '请输入密码'
        elif not user:
            response['msg'] = '用户不存在，请先注册'
        else:
            user = authenticate(username=username, password=password)
            if user:
                _login(request, user)
                if user.is_superuser:
                    response['msg'] = '管理员'
                else:
                    response['msg'] = '普通用户'
            else:
                response['msg'] = '密码错误'
        print(response['msg'])
    return Response(response)


@api_view(['POST', 'GET'])
def signup(request):
    response = {}
    if request.method == 'POST':
        # username = request.POST.get("username")
        # email = request.POST.get("email")
        # password = request.POST.get("password")
        # repeat_password = request.POST.get("repeat_password")

        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        repeat_password = request.POST.get('repeat_password')
        user = User.objects.filter(username=username).first()
        if not username:
            response['msg'] = '请输入用户名'
        elif not email:
            response['msg'] = '请输入邮箱'
        elif not password:
            response['msg'] = '请输入密码'
        elif not repeat_password:
            response['msg'] = '请输入重复密码'
        elif user:
            response['msg'] = '用户已存在'
        elif password != repeat_password:
            response['msg'] = '两次密码输入不一致'
        else:
            response['msg'] = 'success'
            user = User.objects.create_user(
                username=username, email=email, password=password)
            user.save()
        print(response['msg'])
    return Response(response)

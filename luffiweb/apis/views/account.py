# Author: harry.cai
# DATE: 2018/11/6
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import HttpResponse
from apis import models
import uuid

class AuthView(APIView):
    '''
    用户登录认证
    '''
    def options(self, request, *args, **kwargs):
        # 进行预检

        obj = HttpResponse('')
        obj['Access-Control-Allow-Origin'] = '*'
        obj['Access-Control-Allow-Headers'] = "Content-Type"
        return obj

    def post(self, request, *args, **kwargs):
        print(request.data)
        ret = {'code':1000}
        user = request.data.get('user')
        pwd = request.data.get('pwd')
        user_obj = models.Account.objects.filter(user=user, pwd=pwd).first()
        if not user_obj:
            ret['code'] = 1001
            ret['error'] = '用户或密码错误'
        else:
            uid = str(uuid.uuid4())
            # 不存在就创建 存在就更新
            models.UserAuthToken.objects.update_or_create(user=user_obj, defaults={'token': uid})
            ret['token'] = uid
        return Response(ret)
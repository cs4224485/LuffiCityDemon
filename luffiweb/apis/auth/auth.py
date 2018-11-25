# Author: harry.cai
# DATE: 2018/11/8
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from apis import models


class LuffyAuth(BaseAuthentication):
    def authenticate(self, request):
        token = request.query_params.get('token')
        obj = models.UserAuthToken.objects.filter(token=token).first()
        if not obj:
            raise AuthenticationFailed({'code': 1001, 'error': '认证失败'}, )
        return (obj.user.username, obj)

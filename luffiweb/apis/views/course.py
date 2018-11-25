# Author: harry.cai
# DATE: 2018/11/4
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet, ViewSetMixin
from rest_framework.response import Response
from apis import models
from apis.auth.auth import LuffyAuth
from apis.serializers.course import *




class CourseView(ViewSetMixin, APIView):

    def list(self, request, *args, **kwargs):
        '''
        客程列表接口
        :param request:
        :param args:
        :param kwargs:
        :return:
        '''
        ret = {'code': 1000, 'data': None}
        try:
            queryset = models.Course.objects.all()
            ser = CourseSerializer(instance=queryset, many=True)
            ret['data'] = ser.data
        except Exception as e:
            ret['code'] = 1001
            ret['error'] = '获取课程失败'

        return Response(ret)

    def retrieve(self, request, *args, **kwargs):
        '''
        课程详细接口
        :param request:
        :param args:
        :param kwargs:
        :return:
        '''
        ret = {'code': 1000, 'data': None}

        try:
            pk = kwargs.get('pk')
            obj = models.CourseDetail.objects.filter(course_id=pk).first()
            ser = CourseDetailSerializer(instance=obj, many=False)
            ret['data'] = ser.data
        except Exception as e:
            print(e)
            ret['code'] = 1001
            ret['error'] = '获取课程失败'

        return Response(ret)

class MicroView(APIView):
    authentication_classes = [LuffyAuth]
    def get(self, request, *args, **kwargs):
        # 认证通过后返回的元祖
        print(request.user)
        print(request.auth)
        ret = {'code': 1000, 'title': '微职位'}
        return Response(ret)
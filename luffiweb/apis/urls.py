# Author: harry.cai
# DATE: 2018/11/4

from django.urls import path, re_path, include
from apis.views import course, account, schoppingcar, payment, order
urlpatterns = [
    # re_path(r'^course/$', course.CourseView.as_view()),
    # re_path(r'^course/?P<pk>\d+$', course.CourseView.as_view())
    re_path(r'^course/$', course.CourseView.as_view({'get': 'list'})),
    re_path(r'^course/(?P<pk>\d+)/$', course.CourseView.as_view({'get': 'retrieve'})),
    re_path(r'auth/$', account.AuthView.as_view()),
    re_path(r'^micro/$', course.MicroView.as_view()),
    # re_path(r'^shopping/$', schoppingcar.ShoppingCarViewSet.as_view({'post': 'create', 'delete': 'destroy'}))
    re_path(r'^shopping/$', schoppingcar.ShoppingCarViewSet.as_view()),
    re_path(r'^payment/$', payment.PaymentViewSet.as_view()),
    re_path(r'^order/$', order.OrderViewSet.as_view())
]
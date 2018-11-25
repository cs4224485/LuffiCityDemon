# Author: harry.cai
# DATE: 2018/11/24
import json
from rest_framework.viewsets import ViewSetMixin
from rest_framework.views import APIView
from rest_framework.response import Response
from utils.response import BaeResponse
from django_redis import get_redis_connection
from apis.auth.auth import LuffyAuth
from apis import models
from django.core.exceptions import ObjectDoesNotExist
from utils.exception import PricePolicyInvalid
from django.conf import settings
import datetime


class OrderViewSet(APIView):
    def post(self, request, *args, **kwargs):
        '''
        用户点击支付
        :param request:
        :param args:
        :param kwargs:
        :return:
        '''

        '''
          1. 获取用户提交数据
            {
                balance:1000  # 余额
                money:900     # 要支付的钱
            }  
          balance =  request.data.get("balance")
          money = request.data.get("money")
          request.data.get("moneny")
          2  数据验证
                - 大于等于0
                - 个人账户是否有1000贝里  
                
                if request.user.auth.user.balance < balance:
                      账户贝里余额不足
          优惠券ID_LIST = []            
          3 去结算中心活期课程信息
            结算数据：
                    payment_dict = {
                        '2': {
                            course_id:2,
                            'title': 'CRM客户关系管理系统实战开发-专题', 
                            'img': 'CRM.jpg', 'policy_id': '4', 
                            'coupon': {}, 
                            'default_coupon': 0, 
                            'period': 210, 'period_display': '12个月', 'price': 122.0}, 
                        '1': {
                            course_id:2,
                            'title': '爬虫开发-专题', 
                            'img': '爬虫开发-专题.jpg', 
                            'policy_id': '2', 
                            'coupon': {
                                4: {'coupon_type': 0, 'coupon_display': '立减券', 'money_equivalent_value': 40}, 
                                6: {'coupon_type': 1, 'coupon_display': '满减券', 'money_equivalent_value': 60, 'minimum_consume': 100}
                            }, 
                            'default_coupon': 0, 
                            'period': 60, 
                            'period_display': '2个月', 
                            'price': 599.0}
                    }
        
                    global_coupon_dict = {
                        'coupon': {
                            2: {'coupon_type': 1, 'coupon_display': '满减券', 'money_equivalent_value': 200, 'minimum_consume': 500}
                        }, 
                        'default_coupon': 0
                    }
                    ========================================= redis ==============================================
                    redis = {
                        payment_1_2:{
                            course_id:2,
                            'title': 'CRM客户关系管理系统实战开发-专题', 
                            'img': 'CRM.jpg', 'policy_id': '4', 
                            'coupon': {}, 
                            'default_coupon': 0, 
                            'period': 210, 'period_display': '12个月', 'price': 122.0}, 
                        },
                        payment_1_1:{
                            course_id:1,
                            'title': '爬虫开发-专题', 
                            'img': '爬虫开发-专题.jpg', 
                            'policy_id': '2', 
                            'coupon': {
                                4: {'coupon_type': 0, 'coupon_display': '立减券', 'money_equivalent_value': 40}, 
                                6: {'coupon_type': 1, 'coupon_display': '满减券', 'money_equivalent_value': 60, 'minimum_consume': 100}
                            }, 
                            'default_coupon': 0, 
                            'period': 60, 
                            'period_display': '2个月', 
                            'price': 599.0}
                        },
                        payment_global_coupon_1:{
                            'coupon': {
                                2: {'coupon_type': 1, 'coupon_display': '满减券', 'money_equivalent_value': 200, 'minimum_consume': 500}
                            }, 
                            'default_coupon': 0
                        }
                }
            for course_dict in redis的结算数据中获取:
                # 获取课程ID
                # 根据course_id去数据库检查状态
                
                # 获取价格策略
                # 根据policy_id去数据库检查是否依然存在
                
                # 获取使用优惠券ID
                # 根据优惠券ID检查优惠券是否过期
                
                # 获取原价+获取优惠券类型
                    - 立减
                        0 = 原价 - 优惠券金额
                        or
                        折后价 = 原价 - 优惠券金额 
                    - 满减:是否满足最低限制
                        折后价 = 原价 - 优惠券金额    
                    - 折扣
                        折后价 = 原价 *  80/100
                        
          4. 全站优惠券
                - 去数据库校验全站优惠券的合法性
                - 应用优惠券：
                    - 立减
                        0 = 实际支付金额 - 优惠券金额
                        or
                        折后价 = 实际支付金额 - 优惠券金额 
                    - 满减:是否满足最低限制
                        折后价 = 实际支付金额 - 优惠券金额    
                    - 折扣
                        折后价 = 实际支付金额 *  80/100       
          5. 贝里抵扣
          6. 总金额的校验
            实际支付总金额 - 贝里 = money:900
          
          7. 位当前课程生成订单
             -事务：
                 - 订单表创建一条数据
                    - 订单相信创建数据 （有几个商品创建几条） OrderDetail EnrolledCourse
                 - 如果有贝里支付
                    - 贝里金额扣除   Account
                    - 创建交易记录   TransactionsRecord
                 - 优惠券状态更新    CouponRecord
                 # 注意： 如果支付宝支付金额是0 表示订单状态：已支付
                         如果支付宝金额非0， 订单状态：未支付
                            - 生成URL（含订单号）跳转支付宝支付
                            - 回调函数： 更新订单状态
             
        '''
        pass

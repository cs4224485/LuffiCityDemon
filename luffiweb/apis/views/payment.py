# Author: harry.cai
# DATE: 2018/11/19
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


class PaymentViewSet(APIView):
    authentication_classes = [LuffyAuth]
    conn = get_redis_connection('default')

    def post(self, request, *args, **kwargs):
        # 1. 根据课程id从redis中获取响应的课程（含价格）
        # 2. 获取当前用户所有可用的优惠券
        ret = BaeResponse()
        try:
            # 先清空当前用户结算中心的数据
            key_list = self.conn.keys(settings.PAYMENT_KEY % (request.auth.user_id, '*'))
            self.conn.detelte(*key_list)
            self.conn.detelte(settings.PAYMENT_COUPON_KEY % (request.auth.user_id, ))

            payment_dict = {}

            global_coupon_dict = {
                "coupon": {},
                "default_coupon": 0
            }

            # 1. 获取用户要结算课程ID
            course_id_list = request.data.get('courseids')
            for course_id in course_id_list:
                car_key = settings.SHOPPING_CAR_KEY % (request.auth.user_id, course_id)
                # 检查用户要结算的课程是否已经加入到购物车
                if not self.conn.exists(car_key):
                    ret.code = 1001
                    ret.error = '该课程需要先加入购物车'
                    return ret
                # 根据key去redis获取数据

                # 获取标题和图片
                title = self.conn.hget(car_key, 'title').decode('utf-8')
                img = self.conn.hget(car_key, 'img').decode('utf-8')
                # 获取指定的价格策略信息
                default_policy = json.loads(self.conn.hget(car_key, 'policy').decode('utf-8')),
                policy = self.conn.hget(car_key, "default_policy").decode("utf-8")
                policy_info = policy[default_policy]

                payment_course_dict = {
                    'course_id': str(course_id),
                    'title': title,
                    'img': img,
                    'policy_id': policy,
                    'coupon': {},
                    'default_coupon': 0
                }

                payment_course_dict.update(policy_info)
                payment_dict[str(course_id)] = payment_course_dict
            # 获取优惠券
            ctime = datetime.date.today()
            '''
            from django.db.models import Q
            # 使用Q对象构造查询条件
          
            q = Q()
            q1 = Q()
            q1.connector = 'AND'
            q1.children.append(('account', request.auth.user))
            q1.children.append(('status', 0))
            q1.children.append(('coupin__valid_begin_data__lte', ctime))

            q2 = Q()
            q2.connector = 'AND'
            q2.children.append(('coupon__valid_end_date__get', ctime))

            q.add(q1, 'OR')
            q.add(q2, 'OR')
            '''
            coupon_list = models.CouponRecord.objects.filter(account=request.auth.user,
                                                             status=0,
                                                             coupin__valid_begin_data__lte=ctime,
                                                             coupon__valid_end_date__get=ctime)

            for item in coupon_list:
                info = {}
                # 只处理绑定课程的优惠券
                if not item.coupon.object_id:
                    # 优惠券ID
                    coupon_id = item.id

                    # 优惠券类型：满减、折扣、立减
                    coupon_type = item.coupon.coupon_type

                    info = {}
                    info['coupon_type'] = coupon_type
                    info['coupon_display'] = item.coupon.get_coupon_type_display()
                    if coupon_type == 0:  # 立减
                        info['money_equivalent_value'] = item.coupon.money_equivalent_value
                    elif coupon_type == 1:  # 满减券
                        info['money_equivalent_value'] = item.coupon.money_equivalent_value
                        info['minimum_consume'] = item.coupon.minimum_consume
                    else:  # 折扣
                        info['off_percent'] = item.coupon.off_percent

                    global_coupon_dict['coupon'][coupon_id] = info
                    continue
                # 优惠券绑定课程的ID
                coupon_course_id = str(item.coupon.object_id)
                # 优惠卷ID
                coupon_id = item.id
                # 优惠券类型：满减 折扣 立减
                coupon_tye = item.counpon_type
                info['coupon_type'] = coupon_tye
                info['coupin_display'] = item.coupon.get_coupon_type_display()
                if coupon_tye == 0:  # 立减
                    info['money_equivalent_value'] = item.coupon.money_equivalent_value
                elif coupon_tye == 1:  # 满减卷
                    info['money_equivalent_value'] = item.coupon.money_equivalent_value
                    info['minimun_consume'] = item.coupon.minimum_consume
                else:  # 折扣
                    info['off_percent'] = item.coupon.off_percent
                if coupon_course_id not in payment_dict:
                    # 获取到优惠券但是没有购买次课程
                    continue
                # 将会优惠券设置到指定的课程字典中
                payment_dict[coupon_course_id]['coupon'][coupon_id] = info

            # 3. 将绑定优惠券课程+全站优惠券 写入到redis中（结算中心）。
            # 3.1 将绑定优惠券的课程放入redis
            for cid, cinfo in payment_dict.items():
               pay_key = settings.PAYMENT_KEY % (request.auth.user_id, cid)
               cinfo['coupon'] = json.dumps(cinfo['coupon'])
               self.conn.hmset(pay_key, cinfo)
            # 3.2 将全站的优惠券写入redis
            gcoupon_key = settings.PAYMENT_COUPON_KEY % (request.auth.user_id, )
            global_coupon_dict['coupon'] = json.dumps(global_coupon_dict['coupon'])
            self.conn.hmset(gcoupon_key, global_coupon_dict)
        except Exception as e:
            pass

    def patch(self, request, *args, **kwargs):
        ret = BaeResponse()

        try:
            course = request.data.get('courseid')
            course_id = str(course) if course else course
            coupon_id = str(request.data.get('couponid'))
            redis_global_coupon_key = settings.PAYMENT_COUPON_KEY % (request.auth.user_id)

            # 修改全站优惠券
            if not course_id:

                if coupon_id == '0':
                    # 不使用优惠券
                    self.conn.hset(redis_global_coupon_key, 'default_coupon', coupon_id)
                    ret.data= '修改成功'
                    return Response(ret.get_dict)
                # 使用优惠券，请求数据：{"couponid":2}
                coupon_dict = json.loads(self.conn.hget(redis_global_coupon_key, 'coupon').decode('utf-8'))
                # 判断用户选择的优惠券是否合法
                if coupon_id not in coupon_dict:
                    ret.code = 1001
                    ret.error = "全站优惠券不存在"
                    return Response(ret.get_dict)
                # 选择的优惠券合法
                self.conn.hset(redis_global_coupon_key, 'default_coupon', coupon_id)
                ret.data = "修改成功"
                return Response(ret.get_dict)
            # 修改绑定课程优惠券
            redis_payment_key = settings.PAYMENT_KEY % (request.auth.user_id, course_id,) # Luffy_payment_1_1
            # 不使用优惠券
            if course_id == '0':
                self.conn.hset(redis_payment_key,' default_coupon', coupon_id)
                ret.data = '修改成功'
                return Response(ret.get_dict)
            coupon_dict = json.loads(self.conn.hget(redis_payment_key, 'coupon').decode('utf-8'))
            if coupon_id in coupon_dict:
                ret.code = 1010
                ret.error = "课程优惠券不存在"
                return Response(ret.get_dict)
            self.conn.hset(redis_payment_key, 'default_coupon', coupon_id)

        except Exception as e:
            ret.code = 1111
            ret.error = "修改失败"
        return Response(ret.get_dict)

    def get(self, request, *args, **kwargs):
        ret = BaeResponse()
        try:
            # Luffy_payment_1_*
            redis_payment_key = settings.PAYMENT_KEY % (request.auth.user_id, "*")
            redis_global_coupon_key = settings.PAYMENT_COUPON_KEY % (request.auth.user_id,)

            # 1 获取绑定课程的信息
            course_list = []
            for key in self.conn.scan_iter(redis_payment_key):
                info = {}
                data = self.conn.hgetall(key)
                for k, v in data.items():
                    kk = k.decode('utf-8')
                    if kk == "coupon":
                        info[kk] = json.loads(v.decode('utf-8'))
                    else:
                        info[kk] = v.decode('utf-8')

                course_list.append(info)

            # 2. 全站优惠券
            global_coupon_dict = {
                'coupon': json.loads(self.conn.hget(redis_global_coupon_key, 'coupon').decode('utf-8')),
                'default_coupon': json.loads(self.conn.hget(redis_global_coupon_key, 'default_coupon').decode('utf-8'))
            }
            ret.data = {
                'course_list': course_list,
                'global_coupon_dict': global_coupon_dict
            }
        except Exception as e:
            ret.code = 1001
            ret.error = '获取失败'
        return Response(ret.get_dict)
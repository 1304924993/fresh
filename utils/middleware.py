import re

from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.deprecation import MiddlewareMixin

from cart.models import ShoppingCart
from goods.models import Goods
from user.models import User


class TestMiddlware(MiddlewareMixin):

    def process_request(self, request):
        user_id = request.session.get('user_id')
        if user_id:
            user = User.objects.filter(pk=user_id).first()
            request.user = user
            return None
        path = request.path
        if path == '/':
            return None
        not_need_check = [
            '/user/register/', '/user/login/',
            '/goods/index/', '/media/*',
            '/user/logout/', '/goods/detail/.*/',
            '/user/user_center_info/', '/cart/add_cart/',
            '/cart/cart/', '/cart/cart_num/',
            '/cart/change_cart/', '/goods/list/','/static/.*/','/cart/.*/'
        ]
        for not_check in not_need_check:
            if re.match(not_check, path):
                return None
        else:
            return HttpResponseRedirect(reverse('user:login'))


    def process_response(self, request, response):
        user_id = request.session.get('user_id')
        if user_id:
            # 2.同步
            # 判断session中的商品是否存在于数据库中，
            # 如果存在则更新，如果不存在则创建
            # 同步数据库的数据到session中
            session_goods = request.session.get('goods')
            if session_goods:
                for se_goods in session_goods:
                    cart = ShoppingCart.objects.filter(user_id=user_id,
                                                goods_id=se_goods[0]).first()
                    if cart:
                        # 更新商品信息
                        if cart.nums != se_goods[1] or cart.is_select != se_goods[2]:
                            cart.nums = se_goods[1]
                            cart.is_select = se_goods[2]
                            cart.save()
                    else:
                        # 创建
                        ShoppingCart.objects.create(user_id=user_id,
                                                    goods_id=se_goods[0],
                                                    nums=se_goods[1],
                                                    is_select=se_goods[2])

                # 同步数据库中的数据到session中
                db_cart = ShoppingCart.objects.filter(user_id=user_id)
                # 需组装购物车中商品格式为[[goods_id, num, is_select],[goods_id, num, is_select]]
                if db_cart:
                    # [[cart.goods_id, cart.nums, cart.is_select] for cart in db_cart]
                    result = []
                    for cart in db_cart:
                        data = [cart.goods_id, cart.nums, cart.is_select]
                        result.append(data)
                        request.session['goods'] = result
        return response


# class TestMiddlware1(MiddlewareMixin):
#
#     def process_request(self, request):
#
#         return  None
#
#     def process_response(self, request, response):
#         user_id = request.session.get('user_id')
#         if user_id:
#             path = request.path
#             not_need = ['/goods/detail/.*/']
#             goodss = []
#             for i in not_need:
#                 if re.match(i, path):
#                     goodss += path[14:-1]
#             request.session['list'] = goodss
#
#         return response








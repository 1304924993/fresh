from django.http import JsonResponse
from django.shortcuts import render

from cart.models import ShoppingCart
from order.models import OrderInfo, OrderGoods
from user.models import UserAddress
from utils.function import get_order_sn


def place_order(request):
    if request.method == 'GET':
        # 获取当前登录用户
        user = request.user
        carts = ShoppingCart.objects.filter(user=user, is_select=True).all()
        # 计算小计和总价
        total_price = 0
        for cart in carts:
            # 小计金额
            price = cart.goods.shop_price * cart.nums
            cart.goods_price = price
            # 总金额
            total_price += price
        address = UserAddress.objects.filter(user=user)
        return render(request, 'place_order.html',
                      {'shop_carts': carts, 'total_price': total_price, 'user_address': address})


def order(request):
    if request.method == 'POST':
        # 1. 获取收货地址id值
        ad_id = request.POST.get('ad_id')
        # 2. 创建订单
        user_id = request.session.get('user_id')
        # 获取订单编号
        order_sn = get_order_sn()
        # 计算订单金额
        shop_cart = ShoppingCart.objects.filter(user_id=user_id, is_select=True)
        order_mount = 0
        for cart in shop_cart:
            order_mount += cart.goods.shop_price * cart.nums
        # 收货信息
        user_address = UserAddress.objects.filter(pk=ad_id).first()
        order = OrderInfo.objects.create(user_id=user_id,
                                 order_sn=order_sn,
                                 order_mount=order_mount,
                                 address=user_address,
                                 signer_name=user_address.signer_name,
                                 signer_mobile=user_address.signer_mobile)

        # 3. 创建订单详情
        for cart in shop_cart:
            OrderGoods.objects.create(order=order,
                                      goods=cart.goods,
                                      goods_nums=cart.nums)
        # 4. 删除购物车
        shop_cart.delete()
        session_goods = request.session.get('goods')
        for se_goods in session_goods[:]:
            if se_goods[2]:
                session_goods.remove(se_goods)
        request.session['goods'] = session_goods
        return JsonResponse({'code': 200, 'msg': '请求成功'})
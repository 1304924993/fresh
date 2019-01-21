
from django.conf.urls import url

from cart import views

urlpatterns = [
    url(r'^add_cart/', views.add_cart, name='add_cart'),
    # 购物车数量刷新
    url(r'^cart_num/', views.cart_num, name='cart_num'),
    # 购物车页面
    url(r'^cart/', views.cart, name='cart'),
    # 购物车计算价格
    url(r'^cart_price/', views.cart_price, name='cart_price'),
    # 修改数量选择状态
    url(r'^change_cart/', views.change_cart, name='change_cart'),

    url(r'^del_cart/(\d+)/', views.del_cart, name='del_cart'),

]
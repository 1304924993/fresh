
from django.conf.urls import url

from user import views

urlpatterns = [
    # 注册
    url(r'register/', views.register, name='register'),
    # 登录
    url(r'login/', views.login, name='login'),

    url(r'logout/', views.logout, name='logout'),

    url(r'user_info/', views.user_info, name='user_info'),

    url(r'user_site/', views.user_site, name='user_site'),

    url(r'user_order/', views.user_order, name='user_order'),


]

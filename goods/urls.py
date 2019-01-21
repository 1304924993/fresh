from django.conf.urls import url

from goods import views

urlpatterns = [
    # 首页
    url(r'^index/', views.index, name='index'),

    url(r'detail/(\d+)/', views.detail, name='detail'),

    url(r'list/(\d+)/', views.list, name='list'),

    # url()

]
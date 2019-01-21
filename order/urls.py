

from django.conf.urls import url

from order import views

urlpatterns = [
    url('place_order/', views.place_order, name='place_order'),

    url('order/', views.order, name='order'),
]
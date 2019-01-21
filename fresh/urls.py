"""fresh URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.urls import path, include,re_path
from django.contrib.staticfiles.urls import static


from fresh.settings import MEDIA_URL, MEDIA_ROOT, STATICFILES_DIRS
from goods import views
from django.views.static import serve

urlpatterns = [
    path('cart/', include(('cart.urls', 'cart'), namespace='cart')),
    path('goods/', include(('goods.urls', 'goods'), namespace='goods')),
    path('order/', include(('order.urls', 'order'), namespace='order')),
    path('user/', include(('user.urls', 'user'), namespace='user')),

    path('', views.index),
    re_path(r'^static/(?P<path>.*)$', serve, {"document_root": STATICFILES_DIRS[0]}),
    re_path(r'^media/(?P<path>.*)$', serve, {"document_root": MEDIA_ROOT}),
]
urlpatterns += static(MEDIA_URL, document_root=MEDIA_ROOT)
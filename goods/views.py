import time
import datetime

from django.core.paginator import Paginator

from django.shortcuts import render
from django.urls import reverse


from goods.models import GoodsCategory, Goods
from user.models import User


def index(request):
    if request.method == 'GET':
        # cart = GoodsCategory.CATEGORY_TYPE
#         # data = {}
#         # # 循环商品分类
#         # for cate in cart:
#         #     # 获取当前分类下的前四个商品信息
#         #     goods = Goods.objects.filter(category_id=cate[0])[0:4]
#         #     # 组装成键值对，key为商品分类的名称，value为当前分类的商品信息
#         #     data[cate[1]] = goods
#         # return render(request, 'index.html', {'goods_category': data})


        categorys = GoodsCategory.objects.all()
        result = []
        for category in categorys:
            goods = category.goods_set.all()[:4]
            data = [category, goods]
            result.append(data)
        category_type = GoodsCategory.CATEGORY_TYPE
        return render(request, 'index.html',
                      {'result': result, 'category_type': category_type})


def detail(request, id):
    if request.method == 'GET':
        goods = Goods.objects.filter(pk=id).first()
        user_id = request.session.get('user_id')
        if user_id:
            if request.session.get('i'):
                list1 = request.session['i']
                if id not in list1:
                    idd = request.session['i']
                    idd.append(id)
                    request.session['i'] = idd
                    tt = datetime.datetime.now()
                    goods.add_time = tt
                    goods.save()
                else:
                    for li in list1:
                        if id == li:
                            list1.remove(li)
                            break
                    idd = request.session['i']
                    idd.append(id)
                    request.session['i'] = idd
                    tt = datetime.datetime.now()
                    goods.add_time = tt
                    goods.save()

            else:
                request.session['i'] = [id]

        return render(request,'detail.html', {'goods':goods})



def list(request, id):
    if request.method == 'GET':
        page = request.GET.get('page', 1)
        carts = GoodsCategory.objects.filter(pk=id).first()
        goods = carts.goods_set.all()
        paginator = Paginator(goods, 4)
        page = paginator.page(page)
        return render(request, 'list.html', {'page': page})



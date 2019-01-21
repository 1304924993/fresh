

from django.contrib.auth.hashers import make_password, check_password
from django.core.paginator import Paginator
from django.shortcuts import render

# Create your views here.
from django.urls import reverse

from fresh.settings import ORDER_NUMBER
from goods.models import Goods
from order.models import OrderInfo
from user.forms import UserRegisterForm, UserLoginForm, AddressForm
from user.models import User, UserAddress
from django.http import HttpResponseRedirect


def register(request):
    if request.method == 'GET':
        return render(request, 'register.html')
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['user_name']
            password = form.cleaned_data['pwd']
            email = form.cleaned_data['email']
            new_password = make_password(password)
            User.objects.create(username=username,
                                password=new_password,
                                email=email)
            return HttpResponseRedirect(reverse('user:login'))
        else:
            errors = form.errors
            return render(request, 'register.html', {'errors': errors})
def login(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            user = User.objects.filter(username=username).first()
            request.session['user_id'] = user.id
            return HttpResponseRedirect(reverse('goods:index'))
        else:
            errors = form.errors
            return render(request, 'login.html', {'errors': errors})


def logout(request):
    if request.method == 'GET':
        # request.session.flush()
        del request.session['user_id']
        # 删除商品信息
        if request.session.get('goods'):
            del request.session['goods']
        return HttpResponseRedirect(reverse('goods:index'))



def user_site(request):
    if request.method == 'GET':
        user_id = request.session.get('user_id')
        user_address = UserAddress.objects.filter(user_id=user_id)
        return render(request, 'user_center_site.html', {'address':user_address})
    if request.method == 'POST':
        form = AddressForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            address = form.cleaned_data['address']
            postcode = form.cleaned_data['postcode']
            mobile = form.cleaned_data['mobile']
            user_id = request.session.get('user_id')
            UserAddress.objects.create(user_id=user_id,
                                       signer_name=username,
                                       address=address,
                                       signer_postcode=postcode,
                                       signer_mobile=mobile)
            return HttpResponseRedirect(reverse('user:user_site'))
        else:
            error = form.errors
            return render(request, 'user_center_site.html', {'error': error})


def user_order(request):
    if request.method == 'GET':
        user_id = request.session.get('user_id')
        page = request.GET.get('page', 1)
        order_info = OrderInfo.objects.filter(user_id=user_id)
        paginator = Paginator(order_info, ORDER_NUMBER)
        page = paginator.page(page)
        status = OrderInfo.ORDER_STATUS
        return render(request, 'user_order.html', {'page':page, 'status':status})




def user_info(request):
    if request.method == 'GET':
        id = request.session.get('i')
        goods = Goods.objects.filter(id__in=id).order_by('-add_time')[:5]
        return render(request, 'user_center_info.html', {'goods':goods})






import re

from django import forms
from django.contrib.auth.hashers import check_password

from user.models import User


class UserRegisterForm(forms.Form):
    user_name = forms.CharField(max_length=20, min_length=5,
                                required=True, error_messages={
                                'required': '用户名必填',
                                'max_length': '长度不能大于20',
                                'min_length': '长度不能小于5'
                            })
    pwd = forms.CharField(max_length=20, min_length=8,
                          required=True, error_messages={
                          'required': '密码必填',
                          'max_length': '密码长度不能大于20',
                          'min_length': '密码长度不能小于8'
                      })
    cpwd = forms.CharField(max_length=20, min_length=8,
                          required=True, error_messages={
                          'required': '密码必填',
                          'max_length': '密码长度不能大于20',
                          'min_length': '密码长度不能小于8'
                      })
    email = forms.CharField(required=True, error_messages={
                            'required': '邮箱必填'
                        })
    allow = forms.BooleanField(required=True, error_messages={
                            'required': '必须同意协议'
                        })


    def clean(self):
        # 校验用户名是否已存在于数据库
        username = self.cleaned_data.get('user_name')
        user = User.objects.filter(username=username).first()
        if user:
            raise forms.ValidationError({'user_name': '该用于已注册，请去登陆'})
        # 校验密码
        pwd = self.cleaned_data.get('pwd')
        cpwd = self.cleaned_data.get('cpwd')
        if pwd != cpwd:
            raise forms.ValidationError({'pwd': '两次密码不一致'})
        # 校验邮箱
        # email_reg = '^[a-zA-Z0-9_.-]+@[a-zA-Z0-9-]+(\.[a-zA-Z0-9-]+)*\.[a-zA-Z0-9]{2,6}$'
        # email =self.cleaned_data.get('email')
        # if not re.match(email_reg, email):
        #     raise forms.ValidationError('邮箱格式错误')
        return self.cleaned_data


class UserLoginForm(forms.Form):
    username = forms.CharField(max_length=20, min_length=5,
                               required=True, error_messages={
                                'max_length': '用户名长度不能大于20',
                                'min_length': '用户名长度不能小于5',
                                'required': '用户名必填'
                            })
    pwd = forms.CharField(max_length=20, min_length=8,
                               required=True, error_messages={
                                'max_length': '密码长度不能大于20',
                                'min_length': '密码长度不能小于8',
                                'required': '密码必填'
                            })


    def clean(self):
        username = self.cleaned_data.get('username')
        user = User.objects.filter(username=username).first()
        if not user:
            raise forms.ValidationError({'username': '该账号没有注册，请去注册!!!'})
        password = self.cleaned_data.get('pwd')
        if not check_password(password, user.password):
            raise forms.ValidationError({'pwd': '密码错误'})


class AddressForm(forms.Form):
    username = forms.CharField(max_length=5, required=True,
                               error_messages={
                                   'required': '用户名必填',
                                   'max_length': '收件人姓名不能大于5字符'
                               })
    address = forms.CharField(required=True,
                              error_messages={
                                'required': '收货地址必填',
                               })
    postcode = forms.CharField(required=True,
                              error_messages={
                                'required': '邮编必填',
                               })
    mobile = forms.CharField(required=True,
                              error_messages={
                                'required': '手机号必填',
                               })













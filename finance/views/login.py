from django.shortcuts import render,HttpResponse,redirect
from finance.forms.login import LoginForm,LoginSmsForm
from django.http import JsonResponse
from finance.utils.image_code import check_code
from io import BytesIO
from finance import models
from django.db.models import Q

# 密码登录
def login_pwd(request):
    if request.method=='GET':
        form=LoginForm(request)
        return render(request,'login_pwd.html',{'form':form})
    form=LoginForm(request,data=request.POST)
    if form.is_valid():
        form_username=form.cleaned_data['username']
        form_pwd=form.cleaned_data['password']
        # Q允许使用复杂查询
        user_obj=models.UserInfo.objects.filter(Q(email=form_username)|Q(mobile_phone=form_username)).filter(password=form_pwd).first()
        if user_obj:
            # 保存信息进入主页面
            request.session['user_id']=user_obj.id
            request.session['username']=user_obj.username
            request.session.set_expiry(60*60*24*14)
            return redirect('/web/index/')
        form.add_error('username','用户名或密码错误')
    return render(request,'login_pwd.html',{'form':form})

def image_code(request):
    image_obj, code=check_code()
    request.session['image_code']=code
    request.session.set_expiry(60)

    stream=BytesIO()
    image_obj.save(stream,'png')
    return HttpResponse(stream.getvalue())

# 短信验证码登录
def login_sms(request):
    if request.method=='GET':
        form=LoginSmsForm(request)
        return render(request,'login_sms.html',{'form':form})
    form=LoginSmsForm(request,data=request.POST)
    if form.is_valid():
        mobile_phone=form.cleaned_data['mobile_phone']
        user_obj=models.UserInfo.objects.filter(mobile_phone=mobile_phone).first()
        request.session['user_id']=user_obj.id
        request.session['username']=user_obj.username
        request.session.set_expiry(60*60*24*14)
        return redirect('/web/index/')
    return render(request,'login_sms.html',{'form':form})

def logout(request):
    request.session.flush()
    return redirect('/web/index/pwd/')
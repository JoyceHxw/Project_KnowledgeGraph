from django.shortcuts import render,HttpResponse
from finance.forms.account import RegisterModelForm,SendSmsForm
from django.http import JsonResponse

# Create your views here.
# 注册
def register(request):
    if request.method=='GET':
        form=RegisterModelForm(request)
        return render(request,'register.html', {'form':form})
    form=RegisterModelForm(request,data=request.POST)
    if form.is_valid():
        form.save()
        return JsonResponse({'status':True, 'data':'/web/login/pwd/'})
    return JsonResponse({'status':False, 'error':form.errors})

# 发送短信验证码
def send_sms(request):
    form=SendSmsForm(request, data=request.GET)
    if form.is_valid():
        return JsonResponse({'status':True})
    return JsonResponse({'status':False, 'error':form.errors})
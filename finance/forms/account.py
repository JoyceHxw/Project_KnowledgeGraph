from django import forms
from finance import models # 数据库
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from django.conf import settings
import random

# 注册表单
class RegisterModelForm(forms.ModelForm):
    def __init__(self,request,*args, **kwargs):
        super().__init__(*args,**kwargs)
        self.request=request
        for _, field in self.fields.items():
            # 指定相应的小部件，attrs表示形式为文本输入 
            field.widget.attrs['class']='form-control'
            field.widget.attrs['placeholder']='请输入%s'%(field.label,)
    # 指定该表单与哪个模型（Model）相关联
    class Meta:
        model=models.UserInfo
        # 如果模型中没有相应的字段，那么表单就没有与之关联的数据存储位置，confirm_password和code不需要存储
        # 由于继承ModelForm，没有显示地定义email,username的表单字段，自动从模型中生成
        fields=['username','email','password','confirm_password','mobile_phone']

    
    # 表单字段
    mobile_phone=forms.CharField(
        label="手机号",
        # 表示手机号的第一位必须是1，后面跟着3到9中的一个数字，接下来必须是9个数字，$：表示字符串的结尾。
        validators=[RegexValidator(r'^(1[3|4|5|6|7|8|9])\d{9}$', '⼿机号格式错误'),],
    )
    password=forms.CharField(
        label='密码',
        widget=forms.PasswordInput(), # 修改密码的默认显示
        min_length=8,
        max_length=32,
        error_messages={
            # 内置的验证器
            'min_length': "密码长度不能小于8位",
            'max_length': "密码长度不能大于32位",
        },
    )
    confirm_password=forms.CharField(
        label="重复密码",
        widget=forms.PasswordInput(),
        min_length=8,
        max_length=32,
        error_messages={
            'min_length': "密码长度不能小于8位",
            'max_length': "密码长度不能大于32位",
        },
    )
    code=forms.CharField(
        label='验证码',
        widget=forms.TextInput()
    )

    # 自定义验证器
    def clean_username(self):
        # self.cleaned_data是一个字典，它包含了已经通过所有字段验证的数据
        username = self.cleaned_data["username"]
        exists=models.UserInfo.objects.filter(username=username).exists()
        if exists:
            # ValidationError的错误信息存储在表单对象的errors属性中
            raise ValidationError('用户名已存在')
        return username
    
    def clean_email(self):
        email = self.cleaned_data['email']
        exists = models.UserInfo.objects.filter(email=email).exists()
        if exists:
            raise ValidationError('邮箱已存在')
        return email
    
    def clean_password(self):
        pwd = self.cleaned_data["password"]
        return pwd
    
    def clean_confirm_password(self):
        pwd = self.cleaned_data["password"]
        confirm_pwd=self.cleaned_data['confirm_password']
        if pwd!=confirm_pwd:
            raise ValidationError('两次密码不一致')
        return confirm_pwd
    
    def clean_mobile_phone(self):
        mobile_phone = self.cleaned_data['mobile_phone']
        exists = models.UserInfo.objects.filter(mobile_phone=mobile_phone).exists()
        if exists:
            raise ValidationError('⼿机号已注册')
        return mobile_phone
    
    def clean_code(self):
        # 输入的验证码
        code = self.cleaned_data["code"]
        # 使用self.cleaned_data时，如果尝试访问不存在的字段，会引发KeyError异常。
        # 使用self.cleaned_data.get时，如果该键不存在，则默认返回None（或指定的默认值）而不会引发异常。
        mobile_phone=self.cleaned_data.get('mobile_phone')
        if not mobile_phone:
            return code
        # request.session：表示用户的会话数据。Django提供了一个中间件称为"SessionMiddleware"，它负责处理会话数据的存储和管理。
        # 系统生成的验证码
        session_code=self.request.session.get('code')
        if not session_code:
            raise ValidationError("验证码失效或未发送，请重新发送")
        if code!=session_code:
            raise ValidationError("验证码错误，请重新输入")
        return code

# 发送短信验证表单
class SendSmsForm(forms.Form):
    mobile_phone=forms.CharField(
        label="手机号",
        validators=[RegexValidator(r'^(1[3|4|5|6|7|8|9])\d{9}$', '⼿机号格式错误'),]
    )

    def __init__(self,request,*args, **kwargs):
        super().__init__(*args, **kwargs)
        self.request=request

    def clean_mobile_phone(self):
        # 验证短信模板
        # 在html的ajax中定义了url的查询字符串参数
        tpl = self.request.GET.get('tpl')
        template_id = settings.TENCENT_SMS_TEMPLATE.get(tpl)
        if not template_id:
            raise ValidationError('模板不存在')
        
        # 手机号是否存在
        mobile_phone=self.cleaned_data['mobile_phone']
        exists=models.UserInfo.objects.filter(mobile_phone=mobile_phone).exists()
        # 区分登录和注册
        if tpl=='login':
            if not exists:
                raise ValidationError('手机号不存在')
        else:
            if exists:
                raise ValidationError('手机号已存在')
        
        # 生成验证码
        code = random.randrange(1000, 9999)
        print("验证码: ",code)
        # res = send_sms_single('18681693111', template_id, [code, ])
        # if res['result'] != 0:
        #     return HttpResponse(res['errmsg'])
        self.request.session['code']=str(code)
        self.request.session.set_expiry(60)
        return mobile_phone
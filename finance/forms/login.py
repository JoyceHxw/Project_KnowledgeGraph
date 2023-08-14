from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from finance import models

# 密码
class LoginForm(forms.Form):
    # 无关联的model，不需要Meta
    def __init__(self, request, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.request = request
        for _, field in self.fields.items():
            # 指定相应的小部件，attrs表示形式为文本输入 
            field.widget.attrs['class']='form-control'
            field.widget.attrs['placeholder']='请输入%s'%(field.label,)

    username=forms.CharField(
        label='邮箱或手机号',
        error_messages={
        'required': '请输入密码',
        }
    )
    password=forms.CharField(
        label='密码',
        #密码回填，是指在用户提交表单时，如果验证失败，密码字段中输入的值是否会被保留在输入框中，而不是清空。
        widget=forms.PasswordInput(render_value=True),
        error_messages={
        'required': '请输入密码',
        }
    )
    code=forms.CharField(label="图片验证码")
    
    # 验证验证码
    def clean_password(self):
        pwd = self.cleaned_data["password"]
        return pwd
    
    def clean_code(self):
        code = self.cleaned_data["code"]
        session_code=self.request.session.get('image_code')
        if not session_code:
            raise ValidationError('验证码已过期，请重新获取')
        # 不区分大小写和空格
        if code.strip().upper()!=session_code.strip().upper():
            raise ValidationError('验证码输入错误')
        return code
    
# 短信
class LoginSmsForm(forms.Form):
    def __init__(self, request, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.request = request
        for _, field in self.fields.items():
            # 指定相应的小部件，attrs表示形式为文本输入 
            field.widget.attrs['class']='form-control'
            field.widget.attrs['placeholder']='请输入%s'%(field.label,)

    mobile_phone=forms.CharField(
        label='手机号',
        validators=[RegexValidator(r'^(1[3|4|5|6|7|8|9])\d{9}$', '⼿机号格式错误'),]
    )
    code=forms.CharField(
        label='验证码',
        widget=forms.TextInput()
    )
    
    def clean_mobile_phone(self):
        mobile_phone = self.cleaned_data['mobile_phone']
        exists = models.UserInfo.objects.filter(mobile_phone=mobile_phone).exists()
        if not exists:
            raise ValidationError('⼿机号不存在')
        return mobile_phone

    def clean_code(self):
        code = self.cleaned_data['code']
        mobile_phone = self.cleaned_data.get('mobile_phone')
        # ⼿机号不存在，则验证码⽆需再校验
        if not mobile_phone:
            return code

        session_code = self.request.session.get('code') # 从session中获取验证码
        if not session_code:
            raise ValidationError('验证码失效或未发送，请重新发送')

        if code != session_code:
            print("***")
            raise ValidationError('验证码错误，请重新输⼊')
        return code
   
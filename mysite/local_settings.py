# 中⽂设置
LANGUAGE_CODE = "zh-hans"

# 短信类型
TENCENT_SMS_TEMPLATE = {
    # 注册短信模版id
    'register': 1867121,
    # 登录短信模版id
    'login': 1865614,
    'test': 1867121,
}
# 应⽤ID
TENCENT_SMS_APP_ID = "1400839766"
# 应⽤KEY
TENCENT_SMS_APP_KEY = "9f74bb5e5f8a51db75885dac747931ec"
# ⾃⼰填写的签名内容
TENCENT_SMS_SIGN = "黄xw公众号"


# mysql数据库，保存用户信息
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'mysite', # 数据库名字
        'USER': 'root',
        'PASSWORD': '2214563',
        'HOST': '127.0.0.1', # 那台机器安装了MySQL
        'PORT': 3306,
    }
}

# neo4j数据库
NEO4j_DATABASES = {
    'default': {
        'HOST': 'localhost',
        'PORT': 7687,
        'SCHEME':'bolt',
        'USER': 'neo4j',
        'PASSWORD': '2214563hxw',
    }
}

WHITE_REGEX_URL_LIST = [
 '/web/register/',
 '/web/register/sms/',
 '/web/login/pwd/',
 '/web/login/sms/',
 '/web/login/image_code/',
]
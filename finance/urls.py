from django.urls import path
from finance.views import index,login,account,search_all,search_company,\
    search_shareholder,search_executive,search_industry,search_region

urlpatterns = [
    # 注册
    path('register/',account.register, name='register'),
    path('register/sms/',account.send_sms, name='send_sms'),
    # 登录
    path('login/pwd/',login.login_pwd,name='login_pwd'),
    path('login/image_code/',login.image_code,name='image_code'),
    path('login/sms/',login.login_sms,name='login_sms'),
    path('logout/',login.logout,name='logout'),
    # 首页
    path('index/',index.index,name='index'),
    # 所有搜索结果
    path('search_all/',search_all.search_result, name="search_all"),
    # 各实体搜索
    path('search_company_overview/',search_company.search_result_overview, name="search_company_overview"),
    path('search_company_structure/',search_company.search_result_structure, name="search_company_structure"),
    path('search_company_evaluation/',search_company.search_result_evaluation, name="search_company_evaluation"),
    path('search_shareholder/',search_shareholder.search_result, name="search_shareholder"),
    path('search_executive/',search_executive.search_result, name="search_executive"),
    path('search_industry/',search_industry.search_result, name="search_industry"),
    path('search_region/',search_region.search_result, name="search_region"),
]

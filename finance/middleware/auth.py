from django.utils.deprecation import MiddlewareMixin
from finance import models

from django.shortcuts import redirect
from django.conf import settings

from datetime import datetime

class AuthMiddleware(MiddlewareMixin):
    def process_request(self,request):
        # 用户信息
        # 从会话中获取用户的 user_id，如果不存在则返回默认值 0。
        user_id=request.session.get('user_id',0)
        user_obj=models.UserInfo.objects.filter(id=user_id).first()
        request.user_obj=user_obj
        if not request.user_obj:
            if request.path_info in settings.WHITE_REGEX_URL_LIST:
                return None
            return redirect('/web/login/pwd/')


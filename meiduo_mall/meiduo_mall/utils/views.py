from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from meiduo_mall.utils.response_code import RETCODE

class LoginRequiredJSONMixin(LoginRequiredMixin):

    def handle_no_permission(self):
        # 自定义mixin方法,未登录时候返回JSON
        return JsonResponse({'code': RETCODE.SESSIONERR, 'errmsg': '用户未登录'})

# 自定义用户认证系统，可以实现账号或者手机号的登录

from django.contrib.auth.backends import ModelBackend
import re
from django.conf import settings
from users.models import User
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from itsdangerous import BadData
from . import constants

SECRET_KEY = '4p&bas7eul$e-*6+zh*6n39ql=3nxcoa152ch^2-q@(me0i6d3'


def check_verify_email_token(token):
    """
    反序列化token,获取到user
    :param token: 序列化后的用户信息
    :return: user
    """
    s = Serializer(settings.SECRET_KEY, constants.VERIFY_EMAIL_TOKEN_EXPIRES)
    try:
        data = s.loads(token)
    except BadData:
        return None
    else:
        # 从data中取出user_id和email
        user_id = data.get('user_id')
        email = data.get('email')
        try:
            user = User.objects.get(id=user_id, email=email)
        except User.DoesNotExist:
            return None
        else:
            return user


def generate_verify_email_url(user):
    s = Serializer(SECRET_KEY, constants.VERIFY_EMAIL_TOKEN_EXPIRES)
    data = {'user_id': user.id, 'email': user.email}
    token = s.dumps(data)
    return settings.EMAIL_VERIFY_URL + '?token=' + token.decode()


def get_user_by_account(account):
    """
    :param account: 用户名或者手机号
    :return: 用户
    """
    try:
        if re.match(r'^1[3-9]\d{9}$', account):
            user = User.objects.get(mobile=account)
        else:
            user = User.objects.get(username=account)

    except User.DoesNotExist:
        return None
    else:
        return user

class UsernameMobileBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        # 重写用户认证方法
        """
        :param request:
        :param username: 用户名或者手机号
        :param password: 密码明文
        :param kwargs: 额外参数
        :return:
        """
        # 校验传入的是用户名还是手机号
        user = get_user_by_account(username)
        if user and user.check_password(password):
            return user
        else:
            return None


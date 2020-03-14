from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from itsdangerous import BadData
from . import constants

# 使用Django的setts模块种的SECRET_KEY作为传入密钥
SECRET_KEY = '4p&bas7eul$e-*6+zh*6n39ql=3nxcoa152ch^2-q@(me0i6d3'


def check_access_token(access_token_openid):
    #  600秒有效期后如果反解序列，则抛出异常
    # 序列化和反序列化对象的参数必须是一模一样的
    try:
        s = Serializer(SECRET_KEY, constants.ACCESS_TOKEN_EXPIRES)
        data = s.loads(access_token_openid)
    except BadData:
        return None
    else:
        return data.get('openid')




def generate_access_token(openid):
    # 对openid进行序列化编码
    s = Serializer(SECRET_KEY, constants.ACCESS_TOKEN_EXPIRES)
    data = {'openid': openid}
    token = s.dumps(data)
    # 返回类型的bytes类型，需要解码
    return token.decode()


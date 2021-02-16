from flask import request, jsonify, current_app
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

secret_key = 'pbyyds996'


def create_token(api_user):
    # 第一个参数是内部的私钥，这里写在共用的配置信息里了，如果只是测试可以写死
    # 第二个参数是有效期(秒)
    s = Serializer(secret_key, expires_in=3600)
    # 接收用户id转换与编码
    api_user = int(api_user)
    token = s.dumps({"id": api_user}).decode("utf-8")
    return token


def verify_token(token):
    # 参数为私有秘钥，跟上面方法的秘钥保持一致
    s = Serializer(secret_key)
    try:
        # 转换为字典
        data = s.loads(token)
    except Exception:
        return None
    # 拿到转换后的数据，根据模型类去数据库查询用户信息
    return int(data['id'])

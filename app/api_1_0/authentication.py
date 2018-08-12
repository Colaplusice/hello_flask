# encoding=utf-8
from flask_httpauth import HTTPBasicAuth
from flask import g, jsonify
from . import api
from .errors import unthorized, forbidden
from ..models.models import AnonymousUser
from ..models.Users import User

# 在这里初始化,而不是在app创建时

auth = HTTPBasicAuth()


# 密码认证或者令牌认证
@auth.verify_password
def verify_password(email_or_token, password):
    if email_or_token == '':
        g.current_user = AnonymousUser()
        return True

    if password == '':
        g.current_user = User.verify_auth_token(email_or_token)
        g.token_used = True
        return g.current_user is not None

    user = User.query.filter_by(email=email_or_token).first()
    if not user:
        return False
    g.token_used = False
    g.current_user = user
    return user.verify_password(password)


# 认证令牌发送给客户端
@api.route('/token')
def get_token():
    # 匿名用户或者是使用令牌的用户
    if g.current_user.is_anonymous or g.token_used:
        return unthorized('无效的证书')

    return jsonify({'token': g.current_user.
                   generate_auth_token(expiration=3600),
                    'expiration': 3600})


# 用户认证
@api.before_request
@auth.login_required
def before_request():
    if not g.current_user.is_anonymous and \
            not g.current_user.confirmed:
        return forbidden("未认证的用户")


@auth.error_handler
def auth_error():
    return unthorized('无效的证书')

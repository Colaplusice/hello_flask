# encoding=utf-8
# from flask import current_app
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

secret_key = 'hard to gess string'


def Generate_reset_password_token(email, expiration=3600):
    s = Serializer(secret_key, expires_in=expiration)
    return s.dumps({'email': email})


def verify_reset_password(token):
    try:
        s = Serializer(secret_key)
        data = s.loads(token)
        return (data['email'])
    except:
        return None

# token = Generate_reset_password_token('fjl2401')
# print(token)
# print verify_reset_password(token)

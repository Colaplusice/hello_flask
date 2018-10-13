# encoding=utf-8
# from flask import current_app
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from itsdangerous import BadSignature

secret_key = "hard to gess string"


def Generate_reset_password_token(email, expiration=3600):
    s = Serializer(secret_key, expires_in=expiration)
    return s.dumps({"email": email})


def verify_reset_password(token):
    try:
        s = Serializer(secret_key)
        data = s.loads(token)
        return data["email"]
    except BadSignature:
        return None


class SerializeMixin:
    def to_dict(self):
        d = {}
        for column in self.__table__.columns:
            d[column.name] = str(getattr(self, column.name))
            return d


# def make_celery(app):
#     celery = Celery(app.import_name, broker=app.config['CELERY_BROKER_URL'])
#     celery.conf.update(app.config)
#     TaskBase = celery.Task
#     class ContextTask(TaskBase):
#         abstract = True
#         def __call__(self, *args, **kwargs):
#             with app.app_context():
#                 return TaskBase.__call__(self, *args, **kwargs)
#     celery.Task = ContextTask
#     return celery


# token = Generate_reset_password_token('fjl2401')
# print(token)
# print verify_reset_password(token)

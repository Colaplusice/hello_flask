#encoding=utf-8

from functools import wraps
from flask import abort
from flask_login import current_user
from .models import Permisson

#装饰器必须是管理员

def permission_required(permission):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args,**kwargs):
            if not current_user.can(permission):
                abort(403)
            return f(*args,**kwargs)
        return decorated_function
    return decorator

def amdin_required(f):
        return permission_required(Permisson.ADMINISTER)(f)


from flask import jsonify,request,g
from . import api
from .. import db
from ..exceptions import ValidationError
from app.models import Post

def badrequest(message):
    response=jsonify({'error':'bad request','message':message})
    response.status_code=400

    return response


def forbidden(message):
    response=jsonify({'error':'forbidden','message':message})

    response.status_code=403
    return response

def unthorized(message):
    response=jsonify({'error':'unauthorized','message':message})

@api.errorhandler(ValidationError)
def validation_error(e):
    return badrequest(e.args[0])



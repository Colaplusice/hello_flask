from flask import jsonify
from . import api
from ..exceptions import ValidationError


def badrequest(message):
    response = jsonify({"error": "bad request", "message": message})
    response.status_code = 400

    return response


def forbidden(message):
    response = jsonify({"error": "forbidden", "message": message})

    response.status_code = 403
    return response


def unthorized(message):
    pass
    # response = jsonify({'error': 'unauthorized', 'message': message})


@api.errorhandler(ValidationError)
def validation_error(e):
    return badrequest(e.args[0])

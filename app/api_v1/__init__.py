from flask import Blueprint, request
from flask_restplus import Api
from functools import wraps

authorizations = {
    'apiKey': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'Authorization'
    }
}

api_v1 = Blueprint('api_v1', __name__)
api = Api(api_v1, doc='/doc/', authorizations=authorizations, security='apiKey')


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            token = request.headers['Authorization']

        if not token:
            return {'message': 'Token is missing.'}, 401

        return f(*args, **kwargs)

    return decorated


from . import routes



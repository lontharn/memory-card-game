from flask_restplus import fields
from . import api

regis_user = api.model('User', {
    'username': fields.String(required=True, description='user username'),
    'password': fields.String(required=True, description='user password'),
})

user = api.model('User', {
    'id': fields.Integer(description='user Identifier'),
    'username': fields.String(required=True, description='user username'),
    'clicks': fields.Integer(required=False, description='click amount'),
    'my_best': fields.Integer(required=False, description='my best'),
})

card_list = api.model('Card', {
    'id': fields.Integer(description='card Identifier'),
    'value': fields.String(required=True, description='card value'),
    'status': fields.String(required=True, description='card status'),
    'position': fields.String(required=False, description='card position'),
})


card = api.model('Card', {
    'id': fields.Integer(description='card Identifier'),
    'status': fields.String(required=False, description='card status'),
    'value': fields.String(required=False, description='card value'),
    'user_id': fields.String(required=False, description='user Identifier'),
})


board = api.model('Board', {
    'id': fields.Integer(description='board Identifier'),
    'name': fields.String(required=False, description='board name'),
    'global_best': fields.Integer(required=False, description='global best')
})

from flask_restplus import Resource
from flask_jwt import jwt_required
from flask import current_app, abort
from werkzeug.local import LocalProxy

from . import api
from .serializers import user, regis_user, card_list, card, board
from app.models import db, User, Card, Board
from app.jwt import authenticate

import random

_jwt = LocalProxy(lambda: current_app.extensions['jwt'])

ns_user = api.namespace('users', description='User operations')
ns_card = api.namespace('cards', description='Memory card games')
ns_board = api.namespace('board', description='Memory card games')

parser = ns_user.parser()
parser.add_argument('Authorization', type=str, location='headers', required=True)


@ns_user.route('/login')
class UserLogin(Resource):
    """
        User Login Resource
    """
    @ns_user.doc('user login', security=None, body=regis_user)
    def post(self):
        """Get an auth token given user credential"""
        payload = api.payload
        authenticated_user = authenticate(payload['username'], payload['password'])
        access_token = None
        if authenticated_user:
            access_token = _jwt.jwt_encode_callback(authenticated_user)
        else:
            abort(401, 'Invalid credentials')
        return {"access_token": access_token.decode("utf-8")}, 200


@ns_user.route('/')
class UserResourceList(Resource):
    @api.doc('list_users')
    @ns_user.marshal_list_with(user, envelope='users', )
    @jwt_required()
    def get(self):
        """List all users"""
        return [i.serialize for i in User.query.all()]

    @ns_user.doc('create_users', security=None, body=regis_user)
    @ns_user.expect(regis_user)
    @ns_user.marshal_with(regis_user, code=201)
    def post(self):
        """Create a new user"""
        u = User(**api.payload)
        db.session.add(u)
        db.session.commit()
        return u, 201


@ns_user.route('/<int:user_id>')
@ns_user.param('user_id', 'The User identifier')
class UserResource(Resource):
    @ns_user.doc('get_user')
    @ns_user.marshal_with(user)
    @jwt_required()
    def get(self, user_id: int):
        """Fetch a user given resource"""
        return User.query.get_or_404(user_id, 'User not found')

    @ns_user.doc('delete_user')
    @jwt_required()
    def delete(self, user_id):
        """Delete a user given its identifier"""
        u = User.query.get_or_404(user_id, 'User not found')
        db.session.delete(u)
        db.session.commit()
        return '', 204

    @ns_user.doc(body=user)
    @ns_user.expect(user)
    @ns_user.marshal_with(user)
    @jwt_required()
    def put(self, user_id):
        """Update a user given its identifier"""
        user = User.query.get_or_404(user_id, 'User not found')
        user.username = api.payload['username']
        user.password = api.payload['password']
        user.my_best = api.payload['my_best']
        db.session.commit()
        return user, 200


@ns_card.route('/')
class CardResourceList(Resource):
    @ns_card.doc('list_cards')
    @ns_card.marshal_list_with(card_list, envelope='cards')
    @jwt_required()
    def get(self):
        """List all cards"""
        return [i.serialize for i in Card.query.all()]


@ns_card.route('/pick')
class CardPick(Resource):
    @ns_card.doc('Process all cards status by given card id')
    @ns_card.doc(body=card)
    @ns_card.expect(card)
    @ns_card.marshal_with(card)
    @jwt_required()
    def post(self):
        """Update a card status given its identifier"""
        picked_card = Card.query.get_or_404(api.payload['id'], 'Picked card not found')
        flipped_card = Card.query.filter_by(status=Card.STATUS_FLIP).first()
        ret_cards = []
        if not flipped_card:
            # First flip card case
            picked_card.status = Card.STATUS_FLIP
            ret_cards.append(picked_card)
        elif picked_card.value != flipped_card.value:
            # Second flip but it doesn't match with first flip
            picked_card.status = Card.STATUS_CLOSE
            flipped_card.status = Card.STATUS_CLOSE
            ret_cards.extend([picked_card.serialize, flipped_card.serialize])
        else:
            # Second flip that match with first flip
            picked_card.status = Card.STATUS_OPEN
            flipped_card.status = Card.STATUS_OPEN
            ret_cards.extend([picked_card.serialize, flipped_card.serialize])

        u = picked_card.user
        u.clicks = u.clicks + 1
        if u.finished():
            board = Board.query.first_or_404('Board not found')
            if u.my_best == 0 or u.my_best > u.clicks:
                u.my_best = u.clicks
            if board.global_best == 0 or board.global_best > u.my_best:
                board.global_best = u.my_best

            u.clicks = 0

        db.session.commit()

        return ret_cards, 200


@ns_card.route('/new-game')
class CardReset(Resource):
    @ns_card.doc('Reset all cards status and positions')
    @ns_card.doc(body=card)
    @ns_card.expect(card)
    @ns_card.marshal_with(card)
    @jwt_required()
    def post(self):
        """Reset cards status and position"""
        user_id = api.payload['user_id']
        user_obj = User.query.get_or_404(user_id, 'User not found')
        user_obj.clicks = 0
        cards = user_obj.cards
        random.shuffle(cards)
        for i, c in enumerate(cards):
            c.position = i
            c.status = Card.STATUS_CLOSE
        db.session.commit()

        return [c.serialize for c in cards]


@ns_board.route('/')
class BoardResource(Resource):
    @ns_board.doc('get_board')
    @ns_board.marshal_with(board)
    @jwt_required()
    def get(self):
        """Fetch a user given resource"""
        return Board.query.first_or_404('Board not found')

    @ns_board.doc(body=board)
    @ns_board.expect(board)
    @ns_board.marshal_with(board)
    @jwt_required()
    def put(self):
        """Update board given its identifier"""
        payload = api.payload
        board_obj = Board.query.get_or_404(payload['id'], 'Board not found')
        if 'name' in payload:
            board_obj.name = payload['name']

        if 'global_best' in payload:
            board_obj.global_best = payload['global_best']

        db.session.commit()

        return board_obj


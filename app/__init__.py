import logging
import random
from datetime import timedelta

from flask import Flask
from flask_jwt import JWT

from app.api_v1 import api_v1 as api_v1_blueprint
from app.models import db
from config import config
from .models import User, Card, Board
from .jwt import authenticate, identity
from passlib.hash import pbkdf2_sha256


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def create_app(env, additional_settings={}):
    logger.info('Environment in __init__: "%s"', env)
    app = Flask(__name__, instance_relative_config=True, template_folder='templates')
    app.config.from_object(config[env])
    config[env].init_app(app)
    app.config.update(additional_settings)
    app.config['JWT_EXPIRATION_DELTA'] = timedelta(seconds=3600)
    app.config['JWT_AUTH_URL_RULE'] = '/api/v1/auth'
    app.config.update(JWT=JWT(app, authenticate, identity))

    with app.app_context():
        db.init_app(app)
        db.drop_all()
        db.create_all()

        # Initiate User and Card Record
        cards = []
        user = User(username='akekatharn', password=pbkdf2_sha256.hash('password'))
        board = Board(name='Memory Card Game', global_best=20)
        for i in range(1, 7):
            cards.append(Card(value=i, position=0, user=user))
            cards.append(Card(value=i, position=0, user=user))
        random.shuffle(cards)
        for i, c in enumerate(cards):
            c.position = i

        db.session.add(user)
        db.session.add(board)
        db.session.commit()

    # Blueprints
    app.register_blueprint(api_v1_blueprint, url_prefix='/api/v1')

    return app


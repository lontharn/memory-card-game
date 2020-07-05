import logging
import os

from app import create_app
from app.models import db, User, Card, Board

from flask import render_template

logging.basicConfig(level=logging.INFO)
app = create_app((os.getenv("ENV") or "local").lower())


@app.route('/')
def index():
    user = User.query.first_or_404()
    cards = Card.query.with_parent(user).order_by(Card.position).all()
    board = Board.query.first_or_404()
    return render_template(
        'index.html',
        user=user,
        board=board,
        cards=[c.serialize for c in cards]
    )


@app.shell_context_processor
def make_shell_context():
    return dict(app=app, db=db)


@app.cli.command()
def test():
    """Run py.test on the full test suite"""
    import psycopg2
    from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
    import pytest

    con = psycopg2.connect(
        dbname='postgres', 
        user=os.getenv('POSTGRES_USER', 'tester'), 
        host=os.getenv('POSTGRES_HOST', 'db'),
        password=os.getenv('POSTGRES_PASSWORD', '12345'),
    )
    con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    
    try:
        cur = con.cursor()
        cur.execute('CREATE DATABASE ' + 'flaskdb_test')
        cur.close()
        con.close()
    except:
        logging.info("Test database already exists")

    pytest.main(['tests', '-v', '-l'])


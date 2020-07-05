from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class Board(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    global_best = db.Column(db.Integer, default=0)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    clicks = db.Column(db.Integer, default=0)
    my_best = db.Column(db.Integer, default=0)

    def __repr__(self):
        return f'<User {self.username}>'

    @property
    def serialize(self):
        return {
            'id': self.id,
            'username': self.username,
            'password': self.password,
            'clicks': self.clicks,
            'my_best': self.my_best
        }

    def finished(self):
        return all([c.status is Card.STATUS_OPEN for c in self.cards])


class Card(db.Model):
    STATUS_CLOSE = 0
    STATUS_OPEN = 1
    STATUS_FLIP = 2

    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.Integer, nullable=False)
    position = db.Column(db.Integer, nullable=False)
    status = db.Column(db.Integer, default=STATUS_CLOSE)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('cards', lazy=True))

    def __repr__(self):
        return f'<Card {self.id}: {self.value}>'

    @property
    def serialize(self):
        return {
            'id': self.id,
            'value': self.value,
            'position': self.position,
            'status': self.status
        }

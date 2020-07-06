from app.models import User, Card, Board


def test_user_model(session):
    user = User(
        username="username",
        password="password"
    )
    session.add(user)
    session.commit()

    getuser = User.query.filter_by(username=user.username).first()

    assert getuser.username is user.username


def test_card_model(session):
    user = User(
        username="username2",
        password="password2"
    )

    card = Card(
        value=1,
        position=1,
        status=0,
        user=user
    )
    session.add(user)
    session.add(card)
    session.commit()

    getcard = Card.query.filter_by(value=card.value).first()

    assert getcard.value is card.value


def test_board_model(session):
    board = Board(
        name='Memory Card Game',
        global_best=20
    )
    session.add(board)
    session.commit()

    getboard = Board.query.filter_by(name=board.name).first()

    assert getboard.name is board.name

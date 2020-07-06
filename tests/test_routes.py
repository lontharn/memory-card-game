import json
from app.models import User


def test_user_status_code_unauhorised(client):
    response = client.get('/api/v1/users/')
    expected = 401

    assert expected == response.status_code


def test_user_get_token(client):
    raise NotImplementedError


def test_user_response(client):
    raise NotImplementedError


def test_get_card_list_response(client):
    raise NotImplementedError


def test_post_card_pick(client):
    raise NotImplementedError


def test_post_card_new_game(cient):
    raise NotImplementedError


def test_get_card_list(client):
    raise NotImplementedError

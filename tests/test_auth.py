from itsdangerous import json
import pytest
import logging
from flask import g, session
from arena.db import get_db


def test_register(client, app):
    assert client.get('/auth/register').status_code == 200
    response = client.post(
        '/auth/register',
        data={'username': 'a', 'password': 'a'},
    )
    assert 'http://localhost/auth/login' == response.headers['Location']

    with app.app_context():
        my_db = get_db()
        cur = my_db.cursor()
        r = cur.execute("SELECT * FROM game_user WHERE username = 'a'")
        records = [row for row in cur.fetchall()]
        assert records

# @pytest.mark.parametrize(('username', 'password', 'message'), (
#     ('', '', b'username is required.'),
#     ('a', '', b'Password is required.'),
#     ('test', 'test', b'already registered'),
# ))
# def test_register_validate_input(client, username, password, message):
#     my_data={username: username, password: password}
#     response = client.post(
#         '/auth/register',
#         header={'Content-type': "application/x-www-form-urlencoded; charset=UTF-8"},
#         follow_redirects=True,
#         data=my_data,
#     )
#     assert 'http://localhost/auth/login' == response.headers['Location']



def test_logout(client, auth):
    auth.login()

    with client:
        auth.logout()
        assert 'user_id' not in session


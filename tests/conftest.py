from email import header
import os
from asyncio.log import logger

import pytest
import psycopg2

from arena import create_app
from arena.db import init_db, get_db

from Config import TestingConfig

with open(os.path.join(os.path.dirname(__file__), 'data.sql'), 'rb') as f:
    _data_sql = f.read().decode('utf8')

@pytest.fixture
def app():
    # db_fd, db_path = tempfile.mkstemp()
    app = create_app(TestingConfig)
    with app.app_context():
        try:
            init_db()
            db = get_db()
            cur = db.cursor()
            cur.execute(_data_sql)
        except psycopg2.OperationalError as e:
            logger.error("Database must be created!")
            raise e

    yield app



@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def runner(app):
    return app.test_cli_runner()


class AuthActions(object):
    def __init__(self, client):
        self._client = client

    def login(self, username='test', password='test'):
        return self._client.post(
            '/auth/login',
            data={'username': username, 'password': password},
        )

    def logout(self):
        return self._client.get('/auth/logout')


@pytest.fixture
def auth(client):
    return AuthActions(client)

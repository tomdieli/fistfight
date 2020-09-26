import os
import tempfile

import pytest

from flask import current_app

from arena import create_app
from arena.db import init_db


@pytest.fixture(scope='module')
def test_client():
    flask_app = create_app()
    # db_fd, app.config['DATABASE'] = tempfile.mkstemp()
    # app.config['TESTING'] = True

    with flask_app.test_client() as testing_client:
        with flask_app.app_context():
            current_app.logger.info("In the test_client fixture...")
            init_db()
        yield testing_client


def test_get_root(test_client):
#     """Start with a blank database?"""
    response = test_client.get('/')
    current_app.logger.info(response.status_code)
    assert response.status_code == 200
#     #assert b'No entries here so far' in rv.data
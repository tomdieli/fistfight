import os
import tempfile
from subprocess import Popen, PIPE

import pytest

from arena import create_app
from arena.db import init_db


@pytest.fixture
def test_client():
    flask_app = create_app()
    db_fd, flask_app.config['DATABASE'] = tempfile.mkstemp()
    flask_app.config['TESTING'] = True

    with flask_app.test_client() as testing_client:
        with flask_app.app_context():
            init_db()
        yield testing_client

    os.close(db_fd)
    os.unlink(flask_app.config['DATABASE'])


@pytest.fixture
def ws_test_client():
    # flask_app = create_app()
    gunicorn_pid = Popen(['gunicorn',
                            '-k', 'flask_sockets.worker',
                            '-b', '127.0.0.1:5000',
                            'arena:create_app()'], stdout=PIPE)
    # db_fd, flask_app.config['DATABASE'] = tempfile.mkstemp()
    # flask_app.config['TESTING'] = True

    yield gunicorn_pid

    # with flask_app.test_client() as testing_client:
    #     yield testing_client
    #     gunicorn_pid.terminate()
    gunicorn_pid.terminate()

    # os.close(db_fd)
    # os.unlink(flask_app.config['DATABASE'])

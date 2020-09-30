import os
import tempfile

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

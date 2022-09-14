import psycopg2

import pytest
from arena.db import get_db


def test_get_close_db(app):
    with app.app_context():
        db = get_db()
        assert db is get_db()

    with pytest.raises(psycopg2.errors.SyntaxError) as e:
        with app.app_context():
            db = get_db()
            cursor = db.cursor()
            cursor.execute('FOO')
            # print(result)
    print(f'{e.value}')
    # assert 'closed' in str(e.value)


def test_init_db_command(runner, monkeypatch):
    class Recorder(object):
        called = False

    def fake_init_db():
        Recorder.called = True

    monkeypatch.setattr('arena.db.init_db', fake_init_db)
    result = runner.invoke(args=['init-db'])
    assert 'Initialized' in result.output
    assert Recorder.called

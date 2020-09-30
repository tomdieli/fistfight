from .helpers import register, login, logout
from .fixtures import test_client

def test_register(test_client):
    rv = register(test_client , 'snoopy', 'snoop1')
    assert b'User snoopy is already registered' not in rv.data

    rv = register(test_client , 'snoopy', 'snoop1')
    assert b'User snoopy is already registered' in rv.data


def test_login_logout(test_client):
    """Make sure login and logout works."""

    rv = login(test_client , 'snoopy', 'snoop1')
    assert b'Invalid username' in rv.data

    assert register(test_client , 'snoopy', 'snoop1').status_code == 200

    rv = login(test_client , 'snoopy', 'snoop1')
    assert b'Logged in as' in rv.data

    rv = logout(test_client)
    assert b'Log In' in rv.data
    assert b'Register' in rv.data

    rv = login(test_client, 'snoopy', 'snopp1')
    assert b'Invalid password' in rv.data

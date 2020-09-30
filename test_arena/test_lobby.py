from .fixtures import test_client
from .helpers import register, login


def test_lobby(test_client):
    rv = test_client.get('/', follow_redirects=True)
    assert b'Fistfight! - Log In' in rv.data

    assert register(test_client , 'snoopy', 'snoop1').status_code == 200
    assert login(test_client , 'snoopy', 'snoop1').status_code == 200

    rv = test_client.get('/', follow_redirects=True)
    assert b'Fistfight! - Lobby' in rv.data
    # TODO: verify user shown in list
    # assert b'snoopy' in user_list

from .fixtures import test_client
from .helpers import register, login
from .helpers import create_figure, update_figure

def test_game(test_client):
    assert register(test_client , 'snoopy', 'snoop1').status_code == 200
    assert login(test_client , 'snoopy', 'snoop1').status_code == 200

    # test create game
    rv = test_client.post('/game/new_game', data=dict(
        creator=1
    ), follow_redirects=True)
    assert rv.status_code == 200

    # test join game
    assert create_figure(test_client , 'Blorg', 12, 12).status_code == 200
    rv = test_client.get('/game/join/1/user/1', follow_redirects=True)
    assert rv.status_code == 200

    # test play game
    rv = test_client.post('/game/play/1', data=dict(
        figure='Blorg',
    ), follow_redirects=True)
    assert rv.status_code == 200

    # test delete game
    rv = test_client.post('/game/1/delete', follow_redirects=True)
    assert rv.status_code == 200



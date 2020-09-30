from .fixtures import test_client
from .helpers import register, login
from .helpers import create_figure, update_figure

from arena.figure import get_figure_by_name, get_figures_by_user


def test_figure(test_client):

    assert register(test_client , 'snoopy', 'snoop1').status_code == 200
    assert login(test_client , 'snoopy', 'snoop1').status_code == 200

    # Create
    rv = create_figure(test_client , 'Blorg', 12, 12)
    assert rv.status_code == 200
    assert b'Blorg' in rv.data
    
    # Update
    rv = update_figure(test_client , 'Blurg', 12, 12)
    assert rv.status_code == 200
    assert b'Blurg' in rv.data

    # Delete
    rv = test_client.post('/figure/1/delete', follow_redirects=True)
    assert rv.status_code == 200
    assert b'Blurg' not in rv.data


def test_figure_helpers(test_client):
    assert register(test_client , 'snoopy', 'snoop1').status_code == 200
    assert login(test_client , 'snoopy', 'snoop1').status_code == 200
    assert create_figure(test_client , 'Blorg', 12, 12).status_code == 200

    # test get user by name
    blorg = get_figure_by_name('Blorg')
    print(blorg)
    
    # test get_figures_by_user
    blorg = get_figures_by_user(1)
    print(blorg)

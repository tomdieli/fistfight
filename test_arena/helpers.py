def register(test_client, username, password):
    return test_client.post('/auth/register', data=dict(
        username=username,
        password=password
    ), follow_redirects=True)


def login(test_client, username, password):
    return test_client.post('/auth/login', data=dict(
        username=username,
        password=password
    ), follow_redirects=True)


def logout(test_client):
    return test_client.get('/auth/logout', follow_redirects=True)


def create_figure(test_client, figure_name, strength, dexterity):
    return test_client.post('/figure/create', data=dict(
        figure_name=figure_name,
        strength=strength,
        dexterity=dexterity
    ), follow_redirects=True)


def update_figure(test_client, figure_name, strength, dexterity):
    return test_client.post('/figure/1/update', data=dict(
        figure_name=figure_name,
        strength=strength,
        dexterity=dexterity
    ), follow_redirects=True)


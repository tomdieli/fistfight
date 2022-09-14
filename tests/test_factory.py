from arena import create_app
from Config import TestingConfig


def test_config():
    assert not create_app().testing
    assert create_app(TestingConfig).testing


def test_hello(client):
    response = client.get('/')
    print(response.data)
    assert b'<a href="/auth/login">' in response.data



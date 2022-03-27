from gevent import monkey
monkey.patch_all()

from Config import TestingConfig
from arena import create_app, socketio


# TODO: add test config
app = create_app(TestingConfig)

if __name__ == '__main__':
    socketio.run(app)

from gevent import monkey
monkey.patch_all()

from Config import DevelopmentConfig
from arena import create_app, socketio


# TODO: add test config
app = create_app(DevelopmentConfig)

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0')

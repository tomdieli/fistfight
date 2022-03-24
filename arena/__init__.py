# from crypt import methods
import logging
# import redis
from os import environ

from flask import Flask, url_for, render_template
from flask_socketio import SocketIO

from Config import Config

DATABASE_URL = environ.get('DATABASE_URL')
REDIS_URL = environ.get('REDIS_URL')

socketio = SocketIO()

logging.basicConfig(level=logging.INFO)


def create_app(config=None):
    app = Flask(__name__, instance_relative_config=False)

    if config is not None:
        # load the config if passed in
        app.config.from_object(config)

    from . import db
    db.init_app(app)

    from . import auth
    app.register_blueprint(auth.bp)

    from . import figure
    app.register_blueprint(figure.bp)

    from .lobby import lobby as lobby_bp
    app.register_blueprint(lobby_bp)
    app.add_url_rule('/', endpoint='index')

    from .game import game as game_bp
    app.register_blueprint(game_bp)

    socketio.init_app(app, message_queue=REDIS_URL)

    # print(list(app.url_map.iter_rules()))

    return app

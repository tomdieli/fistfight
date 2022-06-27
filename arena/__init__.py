# import logging
from os import environ

from flask import Flask, url_for, render_template
from flask_socketio import SocketIO
from flask_talisman import Talisman

from Config import Config


socketio = SocketIO()


def create_app(config=None):
    app = Flask(__name__, instance_relative_config=False)

    csp = {
    'default-src': [
            '\'self\'',
            '\'unsafe-inline\'',
            'cdnjs.cloudflare.com',
            'cdn.jsdelivr.net',
        ]
    }

    Talisman(app, content_security_policy=csp)

    if config is not None:
        # load the config if passed in
        app.config.from_object(config)
    else:
        app.config.from_object(Config)

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

    socketio.logger = True
    socketio.init_app(app, message_queue=app.config['REDIS_URL'])

    return app

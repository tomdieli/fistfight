import logging
import json
from os import environ

from flask import Flask
from flask_sockets import Sockets


DATABASE_URL = environ.get('DATABASE_URL')

logging.basicConfig(level=logging.INFO)

def create_app(test_config=None):

    app = Flask(__name__, instance_relative_config=False)
    app.config.from_mapping(
        SECRET_KEY = 'dev',
        DATABASE_URL = DATABASE_URL,
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    sockets = Sockets(app)

    from . import db
    db.init_app(app)

    from . import auth
    app.register_blueprint(auth.bp)

    from . import lobby
    app.register_blueprint(lobby.bp)
    app.add_url_rule('/', endpoint='index')

    from . import figure
    app.register_blueprint(figure.bp)
    
    from . import game
    app.register_blueprint(game.bp)

    from . import dealer
    sockets.register_blueprint(dealer.bp)

    return app
import os
import logging
import json

import gevent
import redis
from flask import Flask
from flask_sockets import Sockets

from arena.game import punch
from arena.database import DatabaseServices

REDIS_URL = os.environ['REDIS_URL']
DATABASE_URL = os.environ['DATABASE_URL']
REDIS_CHAN = 'arena'

redis = redis.from_url(REDIS_URL)

logging.basicConfig(level=logging.INFO)

def create_app(test_config=None):
    class Backend(object):
        """Interface for registering and updating WebSocket clients."""

        def __init__(self):
            self.clients = list()
            self.pubsub = redis.pubsub()
            self.pubsub.subscribe(REDIS_CHAN)

        def __iter_data(self):
            for message in self.pubsub.listen():
                data = message.get('data')
                if message['type'] == 'message':
                    app.logger.info(u'Sending message: {}'.format(data))
                    yield data

        def register(self, client):
            """Register a WebSocket connection for Redis updates."""
            self.clients.append(client)

        def send(self, client, data):
            """Send given data to the registered client.
            Automatically discards invalid connections."""
            try:
                client.send(data)
            except Exception:
                self.clients.remove(client)
                raise

        def run(self):
            """Listens for new messages in Redis, and sends them to clients."""
            for data in self.__iter_data():
                for client in self.clients:
                    gevent.spawn(self.send, client, data)

        def start(self):
            """Maintains Redis subscription in the background."""
            gevent.spawn(self.run)

    # create and configure the app
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

    chats = Backend()
    chats.start()

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
    

    @sockets.route('/submit')
    def inbox(ws):
        """Receives incoming player messages, inserts them into Redis."""
        app.logger.info("IN inbox")
        while not ws.closed:
            # TODO: Is therea better way?
            # Sleep to prevent *contstant* context-switches.
            app.logger.info("GETTING message....")
            gevent.sleep(0.1)
            message = ws.receive()
        app.logger.info("GOT message! Type: %s" % type(message))
        app.logger.info(message)

        if message:
            data = json.loads(message)
            print(type(data))
            print("DATA: {}".format(data))
            if data['action'] == "punch":
                punch_result = punch(data["attacker"], data["attackee"])
                data['result_message'] = punch_result["message"]
                data['damage'] = punch_result["damage"]
            elif data["action"] == "join-game":
                app.logger.info("%s is attempting to join the game." % data['figure_name'])
                figure_name = data['figure_name']
                app.logger.info("trying to get game_id %s" % data['game_id'])
                game_id = data['game_id']
                app.logger.info("figure_name: %s, game_id: %s" % (figure_name, game_id))
                with DatabaseServices as db:
                    app.logger.info("lookup fig...")
                    figure = json.loads(db.get_figure_by_name(figure_name))
                with DatabaseServices as db:
                    app.logger.info("adding fig..." % figure)
                    db.add_figure_to_game(figure['id'], game_id)
                with DatabaseServices as db:
                    app.logger.info("getting figs...")
                    players = db.get_figures_by_game_id(game_id)
                    app.logger.info(players)
                with DatabaseServices as db:
                    data["players"] = players
                    data["result_message"] = u'figure_name: {}, game_id: {}'.format(figure, game_id)
            elif data["action"] == "ping":
                data["result_message"] = "pong"
            message = json.dumps(data)
            app.logger.info(u'Inserting message: {}'.format(message))
            redis.publish(REDIS_CHAN, message)

    @sockets.route('/receive')
    def outbox(ws):
        """Sends outgoing chat messages, via `ChatBackend`."""
        # app.logger.info(ws)
        chats.register(ws)

        while not ws.closed:
            # Context switch while `ChatBackend.start` is running in the background.
            gevent.sleep(0.1)

    return app
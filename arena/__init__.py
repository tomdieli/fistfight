import os
import logging
import json

import gevent
import redis
from flask import Flask
from flask_sockets import Sockets

from arena.game import punch

REDIS_URL = os.environ['REDIS_URL']
REDIS_CHAN = 'arena'

redis = redis.from_url(REDIS_URL)

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
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'arena.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    sockets = Sockets(app)

    chats = Backend()
    chats.start()

    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, Waylame!'

    from . import db
    db.init_app(app)

    from . import auth
    app.register_blueprint(auth.bp)

    from . import figure
    app.register_blueprint(figure.bp)
    app.add_url_rule('/', endpoint='index')

    @sockets.route('/submit')
    def inbox(ws):
        """Receives incoming chat messages, inserts them into Redis."""
        while not ws.closed:
            # Sleep to prevent *contstant* context-switches.
            gevent.sleep(0.1)
            message = ws.receive()

            if message:
                data = json.loads(message)
                punch_result = punch(data["attacker"], data["attackee"])
                data['result_message'] = punch_result["message"]
                data['damage'] = punch_result["damage"]
                message = json.dumps(data)
                app.logger.info(u'Inserting message: {}'.format(message))
                redis.publish(REDIS_CHAN, message)

    @sockets.route('/receive')
    def outbox(ws):
        """Sends outgoing chat messages, via `ChatBackend`."""
        chats.register(ws)

        while not ws.closed:
            # Context switch while `ChatBackend.start` is running in the background.
            gevent.sleep(0.1)

    from . import game
    app.register_blueprint(game.bp)


    return app
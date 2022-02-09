from flask import session
from flask_socketio import emit, join_room, leave_room
from .. import socketio

from ..database import DatabaseServices

@socketio.on('joined', namespace='/lobby')
def joined(user):
    # Sent by clients when they enter a room.
    join_room('lobby')
    with DatabaseServices() as dbs:
        users = dbs.get_users()
    emit('joined', {'msg': user + ' has joined the lobby', 'users': users}, room='lobby')


@socketio.on('delete', namespace='/lobby')
def text(message):
    # Sent by a client when the user deletes a game.
    with DatabaseServices() as dbs:
        ret = dbs.delete_game(message['game_id'])
        print(ret)
        games = dbs.get_games()
    emit('delete', 
        {
            'msg': message['user'] + ' has deleted game ' + str(message['game_id']),
            'games': games
        },
        room='lobby')


@socketio.on('create', namespace='/lobby')
def text(message):
    # Sent by a client when the user creates a game.
    with DatabaseServices() as dbs:
        dbs.add_game(message['username'])
        games = dbs.get_games()
    emit('create',
        {
            'msg': message['username'] + ' created a new game',
            'games': games
        },
        room='lobby')


@socketio.on('left', namespace='/lobby')
def left(message):
    # Sent by clients when they leave a room.
    print("LEAFING")
    leave_room('lobby')
    emit('status', {'msg': message}, room='lobby')
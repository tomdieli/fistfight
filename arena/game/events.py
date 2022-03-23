import json

from flask import session, url_for
from flask_socketio import emit, join_room, leave_room

from .. import socketio
from ..database import DatabaseServices
from arena.game_utils import punch, attempt_pull


@socketio.on('joined', namespace='/arena')
def joined(user, game):
    # Sent by clients when they enter a room.
    game_data = game
    game_id = game_data['id']
    join_room('game%s'%game_id)
    with DatabaseServices() as dbs:
        figures = dbs.get_figures_by_game_id(game_id)
    emit('joined',
    {
        'msg': 'user ' + user + ' has come to the table',
        'figures': figures
    },
    room = 'game%s'%game_id)

@socketio.on('starting', namespace='/arena')
def starting(game_id):
    # Sent by clients when they enter a room.
    join_room('game%s'%game_id)


@socketio.on('ready', namespace='/arena')
def ready(game, figure):
    figure_name = figure
    game_data = game
    game_id = game_data['id']
    with DatabaseServices() as db:
        figure = json.loads(db.get_figure_by_name(figure_name))[0]
        db.add_figure_to_game(figure_name, game_id)
        figures = db.get_figures_by_game_id(game_id)
    msg = '%s has entered arena %s' % (figure['figure_name'], game_id)
    emit('ready', {'msg': msg, 'figures': figures}, room='game%d'%game_id)

@socketio.on('start', namespace='/arena')
def start(game_id):
    print('started...')
    emit('start', url_for('game.play', game_id=game_id), room='game%s'%game_id)


@socketio.on('attack', namespace='/arena')
def attack(attacker, attackee, game_id):
    results = punch(attacker, attackee)
    emit('attack', {'msg': results['message'], 'dmg': results['damage'], 'attackee': attackee}, room='game%s'%game_id)


@socketio.on('pull-dagger', namespace='/arena')
def pull_dagger(puller, game_id):
    results = attempt_pull(puller)
    print(f'results: {results}')
    emit('pull-dagger', {'msg': results['message'], 'result': results['result'], 'puller': results['puller']}, room='game%s'%game_id)


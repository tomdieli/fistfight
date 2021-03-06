import random
import json

import psycopg2.extras

from flask import (
    Blueprint, flash, g, redirect, render_template,
    request, url_for, session
)
from werkzeug.exceptions import abort

from arena.auth import login_required
from arena.database import DatabaseServices
from arena.game_utils import punch


bp = Blueprint('game', __name__, url_prefix='/game')


@bp.route('/new_game', methods=('POST',))
@login_required
def create():
    creator = request.form['creator']
    with DatabaseServices() as dbase:
        rows = dbase.add_game(creator)
    return redirect(url_for('lobby.index'), code=307)


@bp.route('/<int:game_id>/delete', methods=('POST',))
@login_required
def delete(game_id):
    with DatabaseServices() as dbase:
        rows = dbase.delete_game(game_id)
    return redirect(url_for('lobby.index'), code=307)


@bp.route('/<int:game_id>/join/<int:user_id>', methods=('POST',))
@login_required
def join(game_id, user_id):
    with DatabaseServices() as dbase:
        my_figures = json.loads(dbase.get_figures_by_user(user_id))
        other_players = json.loads(dbase.get_figures_by_game_id(game_id))
        user = json.loads(dbase.get_username_from_id(user_id))[0]['username']
        current_game = json.loads(dbase.get_game_by_id(game_id))[0]
    return render_template('game/table.html', figures=my_figures,
        game=current_game, user=user, game_owner=current_game['owner'])   # , other_players=other_players


@bp.route('/play/<int:game_id>', methods=('POST','GET'))
@login_required
def play(game_id):
    with DatabaseServices() as dbase:
        figname = request.args.get('figure')
        figure = json.loads(dbase.get_figure_by_name(figname))[0]
        figures = json.loads(dbase.get_figures_by_game_id(game_id))
    return render_template('game/game.html', figures=figures,
                            figure=figure, game_id=game_id)

import random
import json

import psycopg2.extras

from flask import (
    Blueprint, flash, g, redirect, render_template,
    request, url_for, session
)
from werkzeug.exceptions import abort

from arena.auth import login_required
# from arena.database import Database
from arena.database import DatabaseServices

bp = Blueprint('game', __name__, url_prefix='/game')


@bp.route('/new_game', methods=('POST',))
@login_required
def create():
    creator = request.form['creator']
    with DatabaseServices() as dbase:
        rows = dbase.add_game(creator)
        print(rows)
    return redirect(url_for('lobby.index'))


@bp.route('/<int:game_id>/delete', methods=('POST',))
@login_required
def delete(game_id):
    with DatabaseServices() as dbase:
        rows = dbase.delete_game(game_id)
        print(rows)
    return redirect(url_for('lobby.index'))


@bp.route('/<int:game_id>/join/<int:user_id>')     # , methods=('POST',)
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
        print("FIGURE: %s" % figname)
        figure = json.loads(dbase.get_figure_by_name(figname))[0]
        print("FIGURE OBJ: %s" % figure)
        figures = json.loads(dbase.get_figures_by_game_id(game_id))
        
    return render_template('game/game.html', figures=figures, figure=figure, game_id=game_id)

# # TODO: extract these...
# def add_figure(f_name, game_id):
#     with DatabaseServices() as dbase:
#         print(f"Figure: {f_name}")
#         print(f"Game ID: {game_id}")
#         rows = dbase.add_figure_to_game(f_name, game_id)
#         print(rows)
#         figures = json.loads(dbase.get_figures_by_game_id(game_id))
#     return figures


def punch(attack_name, defend_name):
    with DatabaseServices() as dbase:
        attacker = json.loads(dbase.get_figure_by_name(attack_name))[0]
        defender = json.loads(dbase.get_figure_by_name(defend_name))[0]
    rolls = [random.randrange(1, 7) for i in range(0,3)]
    roll_total = sum(rolls)
    if roll_total > attacker["dexterity"]:
        damage = 0
        message = "%s attacks %s but misses with a roll of %s %s" %\
            (attacker["figure_name"], defender["figure_name"], roll_total, rolls)
    else:
        damage = random.randrange(1, 7)
        message = "%s attacks %s and hits with a roll of %s %s. Doing %s damage." %\
            (attacker["figure_name"], defender["figure_name"], roll_total, rolls, damage)

    return { "message": message, "damage": damage }
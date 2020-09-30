import random

import psycopg2.extras

from flask import (
    Blueprint, flash, g, redirect, render_template,
    request, url_for, session
)
from werkzeug.exceptions import abort

from arena.figure import get_figure, get_figure_by_name, get_figures_by_user
from arena.auth import login_required
from arena.db import get_db


bp = Blueprint('game', __name__, url_prefix='/game')


@bp.route('/new_game', methods=('POST',))
@login_required
def create():
    creator = request.form['creator']
    db = get_db()
    cursor = db.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cursor.execute(
        'INSERT INTO game (owner)'
        ' VALUES (%s)',
        (creator,)
    )
    db.commit()
    return redirect(url_for('lobby.index'))


@bp.route('/<int:game_id>/delete', methods=('POST',))
@login_required
def delete(game_id):
    db = get_db()
    cursor = db.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cursor.execute('DELETE FROM game WHERE id = (%s)', (game_id,))
    return redirect(url_for('lobby.index'))


@bp.route('/join/<int:game_id>/user/<int:user_id>', methods=('POST',))
@login_required
def join(game_id, user_id):
    figures = get_figures_by_user(user_id)
    db = get_db()
    cursor = db.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cursor.execute(
        'SELECT username FROM game_user WHERE id = (%s)', (user_id,)
    )
    user_name = cursor.fetchone()

    cursor.execute(
        'SELECT id, owner FROM game WHERE id = (%s)', (game_id,)
    )
    current_game = cursor.fetchone()

    return render_template('game/table.html', figures=figures, game=current_game, user=user_name[0])


@bp.route('/play/<int:game_id>', methods=('POST','GET'))
@login_required
def play(game_id):
    print(request.data)
    figname = request.form.get('figure')
    figure = get_figure_by_name(figname)

    db = get_db()
    cursor = db.cursor(cursor_factory=psycopg2.extras.DictCursor)

    cursor.execute(
        'SELECT figure_name, strength, dexterity'
        ' FROM figure f'
        ' JOIN game g'
        ' ON f.figure_name = ANY (g.players)'
        ' WHERE g.id = %s'
        ' ORDER BY f.dexterity DESC;', (game_id,)
    )
    figures = cursor.fetchall()

    return render_template('game/game.html', figures=figures, figure=figure)


def add_player(f_name, game_id):
    db = get_db()
    cursor = db.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cursor.execute(
        'UPDATE game'
        ' SET players = players || %s::text'
        ' WHERE game.id = %s'
        ' AND %s <> ALL (players);', (f_name, game_id, f_name)
    )
    db.commit()
    figures = []
    cursor.execute(
        'SELECT players from game'
        ' WHERE game.id = %s', (game_id,)
    )
    db.commit()
    figure_list = cursor.fetchall()

    return figure_list[0][0]

def punch(attack_name, defend_name):
    attacker = get_figure_by_name(attack_name)
    defender = get_figure_by_name(defend_name)
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
import random

import psycopg2.extras

from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, session
)
from werkzeug.exceptions import abort

from arena.auth import login_required
from arena.db import get_db

from arena.figure import get_figure, get_figure_by_name

bp = Blueprint('game', __name__)

@bp.route('/join/<int:id>')
@login_required
def join(id):
    figure = get_figure(int(id))

    db = get_db()
    cursor = db.cursor(cursor_factory=psycopg2.extras.DictCursor)

    cursor.execute(
        'SELECT *'
        ' FROM figure p'
        ' WHERE p.id != (%s)'
        ' ORDER BY p.dexterity',
        (figure['id'],)
    )
    figures = cursor.fetchall()

    return render_template('game/lobby.html', figures=figures, figure=figure)


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
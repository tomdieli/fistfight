import random

import psycopg2.extras

from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, session
)
from werkzeug.exceptions import abort

from arena.auth import login_required
from arena.db import get_db

from arena.figure import get_figures_by_user, get_figure

bp = Blueprint('lobby', __name__)

@bp.route('/join/<int:game_id>/user/<int:user_id>')
@login_required
def join(game_id, user_id):
    figures = get_figures_by_user(user_id)
    # user = get_figure(user_id)
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

    return render_template('game/lobby.html', figures=figures, game=current_game, user=user_name[0])



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

@bp.route('/', methods=('GET', 'POST'))
@login_required
def index():
    refresh_games = False
    db = get_db()
    cursor = db.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cursor.execute(
        'SELECT *'
        ' FROM game_user'
    )
    users = cursor.fetchall()
    print(users)
    cursor.execute(
        'SELECT p.id, figure_name, strength, dexterity, user_id, username'
        ' FROM figure p JOIN game_user u ON p.user_id = u.id'
        ' ORDER BY created DESC'
    )
    figures = cursor.fetchall()
    cursor.execute(
        'SELECT *'
        ' FROM game'
        ' ORDER BY created DESC'
    )
    games = cursor.fetchall()
    if request.method == 'POST':
        refresh_games = True
    return render_template('game/index.html', users=users, figures=figures, games=games, refresh_games=False)
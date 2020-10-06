import random
import json

import psycopg2.extras

from flask import (
    Blueprint, redirect, render_template, request,
    url_for, session, current_app
)
from werkzeug.exceptions import abort

from arena.auth import login_required
from arena.db import get_db
# from arena.database import Database
from arena.database import DatabaseServices

bp = Blueprint('lobby', __name__)


@bp.route('/', methods=('GET', 'POST'))
@login_required
def index():
    refresh_games = False
    with DatabaseServices() as dbase:
        users = json.loads(dbase.get_users())
        figures = json.loads(dbase.get_figures())
        games = json.loads(dbase.get_games())
    if request.method == 'POST':
        refresh_games = True
    return render_template('game/index.html', users=users, figures=figures, games=games, refresh_games=False)
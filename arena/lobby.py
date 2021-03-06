import random
import json

import psycopg2.extras

from flask import (
    Blueprint, g, redirect, render_template, request,
    url_for, session, current_app
)
from werkzeug.exceptions import abort

from arena.auth import login_required
from arena.db import get_db
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
    this_user = {
        'username': g.user['username'],
        'id': g.user['id']
    }
    return render_template('game/index.html', users=users, figures=figures,
                            games=games, refreshGames=refresh_games, thisUser=this_user)
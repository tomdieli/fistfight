from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, session
)
from werkzeug.exceptions import abort

from arena.auth import login_required
from arena.db import get_db

from arena.figure import get_figure

bp = Blueprint('game', __name__)

@bp.route('/join/<int:id>')
@login_required
def join(id):
    figure = get_figure(int(id))

    db = get_db()

    figures = db.execute(
        'SELECT p.id, figure_name, strength, dexterity, user_id, username'
        ' FROM figure p JOIN user u ON p.user_id = u.id'
        ' ORDER BY created DESC'
    ).fetchall()

    return render_template('game/lobby.html', figures=figures, figure=figure)

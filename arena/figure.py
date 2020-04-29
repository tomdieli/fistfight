from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from arena.auth import login_required
from arena.db import get_db

bp = Blueprint('figure', __name__)


@bp.route('/')
def index():
    db = get_db()
    figures = db.execute(
        'SELECT p.id, figure_name, strength, dexterity, user_id, username'
        ' FROM figure p JOIN user u ON p.user_id = u.id'
        ' ORDER BY created DESC'
    ).fetchall()
    return render_template('figure/index.html', figures=figures)


@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        figure_name = request.form['figure_name']
        strength = request.form['strength']
        dexterity = request.form['dexterity']
        error = None

        if not figure_name:
            error = 'Name is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO figure (figure_name, strength, dexterity, user_id)'
                ' VALUES (?, ?, ?, ?)',
                (figure_name, strength, dexterity, g.user['id'])
            )
            db.commit()
            return redirect(url_for('figure.index'))

    return render_template('figure/create.html')


def get_figure(id, check_user=True):
    figure = get_db().execute(
        'SELECT p.id, figure_name, strength, dexterity, created, user_id, username'
        ' FROM figure p JOIN user u ON p.user_id = u.id'
        ' WHERE p.id = ?',
        (id,)
    ).fetchone()

    if figure is None:
        abort(404, "Figure id {0} doesn't exist.".format(id))

    if check_user and figure['user_id'] != g.user['id']:
        abort(403)

    return figure


@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    figure = get_figure(id)

    if request.method == 'POST':
        figure_name = request.form['figure_name']
        strength = request.form['strength']
        dexterity = request.form['dexterity']
        error = None

        if not figure_name:
            error = 'Name is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'UPDATE figure SET figure_name = ?, strength = ?, dexterity = ?'
                ' WHERE id = ?',
                (figure_name, strength, dexterity, id)
            )
            db.commit()
            return redirect(url_for('figure.index'))

    return render_template('figure/update.html', figure=figure)


@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    get_figure(id)
    db = get_db()
    db.execute('DELETE FROM figure WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('figure.index'))

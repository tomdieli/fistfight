import psycopg2.extras
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
    cursor = db.cursor(cursor_factory=psycopg2.extras.DictCursor)
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
    return render_template('figure/index.html', figures=figures, games=games)


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
            cursor = db.cursor(cursor_factory=psycopg2.extras.DictCursor)
            print(g.user)
            cursor.execute(
                'INSERT INTO figure (figure_name, strength, dexterity, user_id)'
                ' VALUES ((%s), (%s), (%s), (%s))',
                (figure_name, strength, dexterity, g.user['id'])
            )
            db.commit()
            return redirect(url_for('figure.index'))

    return render_template('figure/create.html')


def get_figure(id, check_user=True):
    db = get_db()
    cursor = db.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cursor.execute(
        'SELECT p.id, figure_name, strength, dexterity, user_id'
        ' FROM figure p JOIN game_user u ON p.user_id = u.id'
        ' WHERE p.id = (%s)',
        (id,)
    )
    figure = cursor.fetchone()

    if figure is None:
        abort(404, "Figure id {0} doesn't exist.".format(id))

    if check_user and figure['user_id'] != g.user['id']:
        abort(403)

    return figure

def get_figure_by_name(name):
    db = get_db()
    cursor = db.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cursor.execute(
        'SELECT *'
        ' FROM figure p'
        ' WHERE p.figure_name = (%s)',
        (name,)
    )
    figure = cursor.fetchone()

    if figure is None:
        abort(404, "Figure id {0} doesn't exist.".format(id))

    return figure


def get_figures_by_user(user_id):
    db = get_db()
    cursor = db.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cursor.execute(
        'SELECT p.id, figure_name, strength, dexterity, user_id'
        ' FROM figure p JOIN game_user u ON p.user_id = u.id'
        ' WHERE u.id = (%s)',
        (user_id,)
    )
    figures = cursor.fetchall()

    if figures is None:
        return []

    return figures


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
            cursor = db.cursor(cursor_factory=psycopg2.extras.DictCursor)
            cursor.execute(
                'UPDATE figure SET figure_name = (%s), strength = (%s), dexterity = (%s)'
                ' WHERE id = (%s)',
                (figure_name, strength, dexterity, id)
            )
            return redirect(url_for('figure.index'))

    return render_template('figure/update.html', figure=figure)


@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    get_figure(id)
    db = get_db()
    cursor = db.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cursor.execute('DELETE FROM figure WHERE id = (%s)', (id,))
    return redirect(url_for('figure.index'))

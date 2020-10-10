from flask import (
    Blueprint, flash, g, redirect,
    render_template, request, url_for
)
from arena.auth import login_required
from arena.database import DatabaseServices

bp = Blueprint('figure', __name__, url_prefix='/figure')

@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        figure_name = request.form['figure_name']
        strength = request.form['strength']
        dexterity = request.form['dexterity']

        # TODO: Determine the best way to validate
        errors = []
        if not figure_name:
            errors += 'Name is required.'
        if errors:
            flash(errors)
        else:
            with DatabaseServices() as dbase:
                rows = dbase.add_figure(figure_name, strength, dexterity, g.user['id'])
                print(rows)
            return redirect(url_for('lobby.index'))

    return render_template('figure/create.html')


@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    if request.method == 'POST':
        figure_name = request.form['figure_name']
        strength = request.form['strength']
        dexterity = request.form['dexterity']
        error = None

        # TODO: Determine the best way to validate
        if not figure_name:
            error = 'Name is required.'

        if error is not None:
            flash(error)
        else:
            with DatabaseServices() as dbase:
                rows = dbase.update_figure(figure_name, strength, dexterity, id)
                print(rows)
            return redirect(url_for('lobby.index'))
    return render_template('figure/update.html', id)


@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    with DatabaseServices() as dbase:
        rows = dbase.delete_figure(id)
        print(rows)
    return redirect(url_for('lobby.index'))
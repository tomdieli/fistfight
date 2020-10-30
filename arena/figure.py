import json

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
        strength = int(request.form['strength'])
        dexterity = int(request.form['dexterity'])

        # TODO: validate name using db services
        error = None
        if (strength + dexterity) != 24:
            error = 'You must divide exactly 8 points between your stats. not %s and %s' % (strength,dexterity)
        if error:
            flash(error)
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
        strength = int(request.form['strength'])
        dexterity = int(request.form['dexterity'])
        error = None

        # TODO: Form requires field, but check for duplicate figname?
        if (strength + dexterity) != 24:
            error = 'You must divide exactly 8 points between your stats. not %s and %s' % (strength,dexterity)
        if error:
            flash(error)
        else:
            with DatabaseServices() as dbase:
                rows = dbase.update_figure(figure_name, strength, dexterity, id)
            return redirect(url_for('lobby.index'))

    with DatabaseServices() as dbase:
        figure_str = dbase.get_figure_by_id(id)
        figure = json.loads(figure_str)[0]
    return render_template('figure/update.html', figure=figure)


@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    with DatabaseServices() as dbase:
        rows = dbase.delete_figure(id)
    return redirect(url_for('lobby.index'))
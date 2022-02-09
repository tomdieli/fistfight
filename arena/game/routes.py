import json

from flask import g, redirect, render_template, request, url_for, session

from arena.auth import login_required
from arena.database import DatabaseServices

from . import game


@game.route('/<int:game_id>/join/<int:user_id>', methods=('POST','GET'))
@login_required
def join(game_id, user_id):
    print(f'g ${game_id}, u ${user_id}')
    with DatabaseServices() as dbase:
        my_figures = json.loads(dbase.get_figures_by_user(user_id))
        user = json.loads(dbase.get_username_from_id(user_id))[0]['username']
        current_game = json.loads(dbase.get_game_by_id(game_id))[0]
    return render_template('game/table.html', figures=my_figures,
        game=current_game, user=user)


@game.route('/play/<int:game_id>', methods=('POST','GET'))
@login_required
def play(game_id):
    with DatabaseServices() as dbase:
        figname = request.args.get('figure')
        figure = json.loads(dbase.get_figure_by_name(figname))[0]
        figures = json.loads(dbase.get_figures_by_game_id(game_id))
    return render_template('game/game.html', figures=figures,
                            figure=figure, game_id=game_id)

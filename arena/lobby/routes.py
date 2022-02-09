import json

from flask import g, redirect, render_template, request, url_for, session

from arena.auth import login_required
from arena.database import DatabaseServices

from . import lobby

@lobby.route('/', methods=('GET', 'POST'))
@login_required
def index():
    with DatabaseServices() as dbase:
        figures = json.loads(dbase.get_figures())
        games = json.loads(dbase.get_games())
        users = json.loads(dbase.get_users())
    this_user = {
        'username': g.user['username'],
        'id': g.user['id']
    }
    return render_template(
        'game/index.html',
        figures=figures,
        games=games,
        users = users,
        thisUser=this_user,
        room='lobby'
    )

# @lobby.route("/all-links", methods=('GET',))
# def all_links():
#     links = []
#     for rule in app.url_map.iter_rules():
#         if len(rule.defaults) >= len(rule.arguments):
#             url = url_for(rule.endpoint, **(rule.defaults or {}))
#             links.append((url, rule.endpoint))
#     return render_template("all_links.html", links=links)

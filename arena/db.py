import psycopg2

import click
from flask import current_app, g
from flask.cli import with_appcontext


def get_db():
    if 'db' not in g:
        print(f"DB: {current_app.config['DATABASE_URL']}")
        g.db = psycopg2.connect(current_app.config['DATABASE_URL'])
        g.db.set_session(autocommit=True)
    return g.db


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()


def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)


def init_db():
    db = get_db()
    cursor = db.cursor()
    with current_app.open_resource('schema.sql') as f:
        cursor.execute(f.read().decode('utf8'))


def select_rows(query):
    db = get_db()
    cursor = db.cursor()
    cursor.execute(query)
    records = [row for row in cursor.fetchall()]
    cursor.close()
    return records



@click.command('init-db')
@with_appcontext
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')



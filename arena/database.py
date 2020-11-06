import psycopg2
import json
import datetime
from psycopg2.extras import DictCursor, RealDictCursor, RealDictRow

import click
from flask import current_app, g
from flask.cli import with_appcontext

from .db import get_db


def datetime_converter(o):
        if isinstance(o, datetime.datetime):
            return o.__str__()


def select_rows(db_conn, query, qargs=None):
    """Run a SQL query to select rows from table."""
    cursor = db_conn.cursor(cursor_factory=RealDictCursor)
    cursor.execute(query, qargs)
    return json.dumps(cursor.fetchall(), default=datetime_converter)


def update_rows(db_conn, query, qargs):
    """Run a SQL query to update rows in table."""
    cursor = db_conn.cursor()
    cursor.execute(query, qargs)
    db_conn.commit()
    return f"{cursor.rowcount} rows updated."


def insert_rows(db_conn, query, qargs):
    """Run a SQL query to update rows in table."""
    cursor = db_conn.cursor()
    cursor.execute(query, qargs)
    db_conn.commit()
    return f"{cursor.rowcount} rows inserted."


def delete_rows(db_conn, query, qargs):
    """Run a SQL query to update rows in table."""
    cursor = db_conn.cursor()
    cursor.execute(query, qargs)
    db_conn.commit()
    return f"{cursor.rowcount} rows deleted."


class DatabaseServices:
    """Fistfight-specific database services."""

    def __init__(self):
        self.database = get_db()

    def __enter__ (self):
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        if exc_type:
            print(f'exc_type: {exc_type}')
            print(f'exc_value: {exc_value}')
            print(f'exc_traceback: {exc_traceback}')
            self.database.rollback()
    
    def get_users(self):
        query = 'SELECT * FROM game_user'
        return select_rows(self.database, query)

    def get_figures(self):
        query = 'SELECT * FROM figure'
        return select_rows(self.database, query)

    def get_games(self):
        query = 'SELECT * FROM game'
        return select_rows(self.database, query)

    def add_figure(self, name, st, dx, uid):
        query=\
        r'INSERT INTO figure (figure_name, strength, dexterity, user_id)'\
        r' VALUES (%s, %s, %s, %s)'
        qargs = (name, st, dx, uid)
        return insert_rows(self.database, query, qargs)

    def update_figure(self, figure_name, strength, dexterity, id):
        query=\
        r'UPDATE figure'\
        r' SET figure_name = (%s), strength = (%s), dexterity = (%s)'\
        r' WHERE id = (%s)'
        qargs = (figure_name, strength, dexterity, id)
        return update_rows(self.database, query, qargs)

    def delete_figure(self, id):
        query = r'DELETE FROM figure WHERE id = (%s)'
        qargs = (id,)
        return delete_rows(self.database, query, qargs)

    def get_figures_by_user(self, user_id):
        query=\
        r'SELECT p.id, figure_name, strength, dexterity, user_id'\
        r' FROM figure p JOIN game_user u ON p.user_id = u.id'\
        r' WHERE u.id = (%s)'
        qargs = (user_id,)
        return select_rows(self.database, query, qargs)

    def get_figure_by_name(self, figure_name):
        query =\
            r'SELECT id, figure_name, strength, dexterity'\
            r' FROM figure p'\
            r' WHERE p.figure_name = (%s)'
        qargs = (figure_name,)
        return select_rows(self.database, query, qargs)

    def get_figure_by_id(self, id):
        query =\
            r'SELECT p.id, figure_name, strength, dexterity'\
            r' FROM figure p'\
            r' WHERE p.id = (%s)'
        qargs = (id,)
        return select_rows(self.database, query, qargs)

    def get_user_by_id(self, user_id):
        query = (
            r'SELECT id, username'\
            r' FROM user u'\
            r' WHERE u.id = (%s)'
        )
        qargs = (user_id,)
        return select_rows(self.database, query, qargs)

    def add_game(self, creator):
        query = (
            r'INSERT INTO game (owner)'
            r' VALUES (%s)'
        )
        qargs = (creator,)
        return insert_rows(self.database, query, qargs)

    def delete_game(self, game_id):
        query = r'DELETE FROM game WHERE id = (%s)'
        qargs = (game_id,)
        return delete_rows(self.database, query, qargs)

    def get_username_from_id(self, user_id):
        query = r'SELECT username FROM game_user WHERE id = (%s)'
        qargs = (user_id,)
        return select_rows(self.database, query, qargs)
        
    def get_game_by_id(self, game_id):
        query = r'SELECT id, owner FROM game WHERE id = (%s)'
        qargs = (game_id,)
        return select_rows(self.database, query, qargs)

    def get_figures_by_game_id(self, game_id):
        query = (
            'SELECT f.id, figure_name, strength, dexterity'
            ' FROM figure f'
            ' JOIN game g'
            ' ON f.figure_name = ANY (g.players)'
            ' WHERE g.id = %s'
            ' ORDER BY f.dexterity DESC;'
        )
        qargs = (game_id,)
        return select_rows(self.database, query, qargs)

    def add_figure_to_game(self, figure_name, game_id):
        query = (
            'UPDATE game'
            ' SET players = players || %s::text'
            ' WHERE game.id = %s'
            ' AND %s <> ALL (players);'
        )
        qargs = (figure_name, game_id, figure_name)
        return update_rows(self.database, query, qargs)
    

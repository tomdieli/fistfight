import psycopg2
import json
import datetime
from psycopg2.extras import DictCursor, RealDictCursor, RealDictRow

from flask import current_app, g

DATABASE_URL="postgresql://tom:k1k1Dee@localhost/arena"

def datetime_converter(o):
        if isinstance(o, datetime.datetime):
            return o.__str__()

class Database:
    """Generic interface to PostgreSQL Database."""

    def __init__(self, db_url=DATABASE_URL):
        self.database_url = db_url
        self.conn = None

    def connect(self):
        if self.conn is None:
            self.conn = psycopg2.connect(self.database_url)
            self.conn.set_session(autocommit=True)
        # if 'db' not in g:
        #     g.db = self.conn
            

    def select_rows(self, query, qargs=None):
        """Run a SQL query to select rows from table."""
        self.connect()
        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(query, qargs)
            return json.dumps(cur.fetchall(), default=datetime_converter)
    
    def update_rows(self, query, qargs):
        """Run a SQL query to update rows in table."""
        self.connect()
        with self.conn.cursor() as cur:
            cur.execute(query, qargs)
            self.conn.commit()
            return f"{cur.rowcount} rows updated."

    def insert_rows(self, query, qargs):
        """Run a SQL query to update rows in table."""
        self.connect()
        with self.conn.cursor() as cur:
            cur.execute(query, qargs)
            self.conn.commit()
            return f"{cur.rowcount} rows inserted."

    def delete_rows(self, query, qargs):
        """Run a SQL query to update rows in table."""
        self.connect()
        with self.conn.cursor() as cur:
            cur.execute(query, qargs)
            self.conn.commit()
            return f"{cur.rowcount} rows deleted."


# DB services
# TODO: extract these
class DatabaseServices:
    """Fistfight-specific database services."""

    def __init__(self):
        self.database = Database()

    def __enter__ (self):
        # Code to start a new transaction
        self.database.connect()
        if 'db' not in g:
            g.db = self.database.conn
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        if exc_type:
            print(f'exc_type: {exc_type}')
            print(f'exc_value: {exc_value}')
            print(f'exc_traceback: {exc_traceback}')
            self.database.conn.rollback()

        db = g.pop('db', None)
        if db is not None:
            db.close()
    
    def get_users(self):
        query = 'SELECT * FROM game_user'
        return self.database.select_rows(query)

    def get_figures(self):
        query = 'SELECT * FROM figure'
        return self.database.select_rows(query)

    def get_games(self):
        query = 'SELECT * FROM game'
        return self.database.select_rows(query)

    def add_figure(self, name, st, dx, uid):
        query=\
        r'INSERT INTO figure (figure_name, strength, dexterity, user_id)'\
        r' VALUES (%s, %s, %s, %s)'
        qargs = (name, st, dx, uid)
        return self.database.insert_rows(query, qargs)

    def update_figure(self, figure_name, strength, dexterity, id):
        query=\
        r'UPDATE figure'\
        r' SET figure_name = (%s), strength = (%s), dexterity = (%s)'\
        r' WHERE id = (%s)'
        qargs = (figure_name, strength, dexterity, id)
        return self.database.update_rows(query, qargs)

    def delete_figure(self, id):
        query = r'DELETE FROM figure WHERE id = (%s)'
        qargs = (id,)
        return self.database.delete_rows(query, qargs)

    def get_figures_by_user(self, user_id):
        query=\
        r'SELECT p.id, figure_name, strength, dexterity, user_id'\
        r' FROM figure p JOIN game_user u ON p.user_id = u.id'\
        r' WHERE u.id = (%s)'
        qargs = (user_id,)
        return self.database.select_rows(query, qargs)

    def get_figure_by_name(self, figure_name):
        query =\
            r'SELECT *'\
            r' FROM figure p'\
            r' WHERE p.figure_name = (%s)'
        qargs = (figure_name,)
        return self.database.select_rows(query, qargs)

    def add_game(self, creator):
        query = (
            r'INSERT INTO game (owner)'
            r' VALUES (%s)'
        )
        qargs = (creator,)
        return self.database.insert_rows(query, qargs)

    def delete_game(self, game_id):
        query = r'DELETE FROM game WHERE id = (%s)'
        qargs = (game_id,)
        return self.database.delete_rows(query, qargs)

    def get_username_from_id(self, user_id):
        query = r'SELECT username FROM game_user WHERE id = (%s)'
        qargs = (user_id,)
        return self.database.select_rows(query, qargs)
        
    def get_game_by_id(self, game_id):
        query = r'SELECT id, owner FROM game WHERE id = (%s)'
        qargs = (game_id,)
        return self.database.select_rows(query, qargs)

    def get_figures_by_game_id(self, game_id):
        query = (
            'SELECT figure_name, strength, dexterity'
            ' FROM figure f'
            ' JOIN game g'
            ' ON f.figure_name = ANY (g.players)'
            ' WHERE g.id = %s'
            ' ORDER BY f.dexterity DESC;'
        )
        qargs = (game_id,)
        return self.database.select_rows(query, qargs)

    def add_figure_to_game(self, figure_id, game_id):
        query = (
            'UPDATE game'
            ' SET players = players || %s::text'
            ' WHERE game.id = %s'
            ' AND %s <> ALL (players);'
        )
        qargs = (figure_id, game_id)
        return self.database.update_rows(query, qargs)
    

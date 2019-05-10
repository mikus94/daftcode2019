# coding: utf-8
"""
Zadanie rekrutacyjne Daftcode, Notif.AI.
Zadanie 1.
Autor: Mikolaj Gagatek
email: mikolaj.gagatek@gmail.com
"""
import sqlite3

import click
from flask import current_app, g
from flask.cli import with_appcontext

TABLE_NAME = 'tasks'


def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)


def init_db():
    """
    Initializer of SQLite3 Database.
    Returns:

    """
    db = get_db()
    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))


@click.command('init-db')
@with_appcontext
def init_db_command():
    """
    Clear the existing data and create new tables.
    """
    init_db()
    click.echo('Initialized the database.')


def get_db():
    """
    Method retrieving db connection.

    Returns:
        Db connection.

    """

    def dict_factory(cursor, row):
        """
        Creates dict from row.

        Args:
            cursor: DB cursor.
            row: Row.

        Returns:
            dict: Dict of results.
        """
        d = {}
        for idx, col in enumerate(cursor.description):
            d[col[0]] = row[idx]
        return d

    if '_database' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = dict_factory
    return g.db


def close_db(_):
    """
    Closing database connection.
    """
    db = g.pop('_database', None)
    if db is not None:
        db.close()


def db_query(query, args=(), one=False):
    """
    Querying Db.

    Args:
        query: Query
        args: Arguments to query.
        one: Indicator if only 1 result.

    Returns:
        Result query.
    """
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv


def db_get_all_tasks():
    """
    Getting all the tasks in database.

    Returns:
        (list): Returns list of tasks.
    """
    sql = "SELECT * FROM {};".format(TABLE_NAME)
    return db_query(sql)


def db_insert_task(task):
    """
    Insert new task into database.

    Args:
        task (dict): Dictionary with filled task fields.

    Returns:
        (int): Id of inserted row.
    """
    # create query
    cols = ', '.join(task.keys())
    place_holders = ', '.join('?' * len(task))
    sql = ("INSERT INTO {} ({}) VALUES ({})"
           .format(TABLE_NAME, cols, place_holders))
    db = get_db()
    # get used cursor to obtain the row id
    cursor_used = db.execute(sql, tuple(task.values()))
    task_id = cursor_used.lastrowid
    db.commit()
    return task_id


def db_update_task(task):
    """
    Update task title, done and done_date.

    Args:
        task (tuple): Tuple containing (title, done, done_date, id)
    """
    sql = ('''
              UPDATE {}
              SET title = ? ,
                  done = ? ,
                  done_date = ?
              WHERE id = ?
            '''.format(TABLE_NAME))
    cur = get_db()
    cur.execute(sql, task)
    cur.commit()


def db_delete_task(task_id):
    """
    Deletes task.

    Args:
        task_id (int): Id of task to be deleted.
    """
    sql = "DELETE FROM {} WHERE id=?".format(TABLE_NAME)
    cur = get_db()
    cur.execute(sql, (task_id,))
    cur.commit()


def db_get_task(task_id):
    """
    Getting task from database.

    Args:
        task_id (int): Id of task to get.

    Returns:
        Dict of task.
    """
    sql = "SELECT * FROM {} WHERE id=?".format(TABLE_NAME)
    return db_query(sql, (task_id,), True)

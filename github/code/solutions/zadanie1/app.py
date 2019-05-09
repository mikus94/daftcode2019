# coding: utf-8
"""
Zadanie rekrutacyjne Daftcode, Notify.AI.
Zadanie 1.
Autor: Mikolaj Gagatek
email: mikolaj.gagatek@gmail.com
"""
import sqlite3
import os
import datetime

from flask import Flask, request, g, jsonify, abort
app = Flask(__name__)

# database located in this directory with database.db name
DATABASE = os.path.join(os.getcwd(), 'database.db')
# name of a table in database
TABLE_NAME = 'tasks'


################################################################################
# DATABASE FUNCTIONS
################################################################################

def db_init():
    """
    Initializer of SQLite3 Database.
    """
    with app.app_context():
        db = db_get()
        with app.open_resource('db.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()


def db_get():
    """
    Method retriving db connection.
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

    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = dict_factory
    return db


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
    cur = db_get().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv


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
    # insert into table
    db = db_get()
    # get used cursor to obtain the row id
    cursor_used = db.execute(sql, tuple(task.values()))
    task_id = cursor_used.lastrowid
    # commit the transaction
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
    cur = db_get()
    cur.execute(sql, task)
    cur.commit()


def db_delete_task(task_id):
    """
    Deletes task
    Args:
        task_id (int): Id of task to be deleted.
    """
    sql = "DELETE FROM {} WHERE id=?".format(TABLE_NAME)
    cur = db_get()
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

################################################################################
# Utility functions
################################################################################


def current_date():
    """
    Obtaining current date and time.
    Returns:
        (str): Current date and time.
    """
    return datetime.datetime.now().replace(microsecond=0)


################################################################################
# Flask functions and views.
################################################################################

@app.teardown_appcontext
def close_connection(_):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

################################################################################
# /todolist


@app.route('/todolist', methods=['GET', 'POST'])
def tasks_list():
    """
    Todolist view form.
    Returns:
        View or uploads new task.
    """
    # request was get
    if request.method == 'GET':
        return get_tasks_list()
    # request was post
    if request.method == 'POST':
        return post_tasks_list()


def get_tasks_list():
    """
    Executes view for presenting all the tasks.
    Returns:
        View with all the tasks as jsons.
    """
    # get all the tasks
    result = db_query("SELECT * FROM {};".format(TABLE_NAME))
    # return their jsons
    return jsonify(result)


def post_tasks_list():
    """
    Executes inserting new task to todolist.
    Returns:
        View with updated task list.
    """
    # get all the data needed
    data = request.get_json()
    host_addr = str(request.remote_addr)
    title = data.get('title', None)
    done = data.get('done', False)
    # get date and in case null replace it with None
    done_date = data.get('done_date', None)
    # get current time
    now = current_date()
    #  check if title was given
    if title is None:
        return abort(400)
    # check if done date is declared while task is not done
    if done is False and done_date is not None:
        return abort(400)
    # check if task was done now or date was declared
    if done and done_date is None:
        done_date = now
    # create a row to db
    row = {
        "title": title,
        "done": done,
        "author_ip": host_addr,
        "created_date": now,
        "done_date": done_date
    }
    # execute insert
    task_id = db_insert_task(row)
    # return jsonified view
    return jsonify(task_id=task_id)

################################################################################
# /todolist/<task_id>


@app.route('/todolist/<int:task_id>', methods=['PATCH', 'GET', 'DELETE'])
def list_id(task_id):
    """
    Executes view of given id. With method Patch it modifies it, with Get it
    shows it.

    Args:
        task_id (int): Id of a task.

    Returns:
        View.
    """
    # request was patch
    if request.method == 'PATCH':
        return patch_list_id(task_id)
    # request was get
    if request.method == 'GET':
        return get_list_id(task_id)
    # request was delete
    if request.method == 'DELETE':
        return delete_list_id(task_id)


def delete_list_id(task_id):
    """
    Executes view by deleting existing task.
    Args:
        task_id (int): Id of task to be deleted.

    Returns:
        Http code 204 in case of success or 404 otherwise.
    """
    # check if task exists
    task = db_get_task(task_id)
    if task is None:
        return abort(404)
    # task exists so delete it
    db_delete_task(task_id)
    return '', 204


def get_list_id(task_id):
    """
    Executes view by presenting its json on website.
    Args:
        task_id (int): Id of task to be presented.

    Returns:
        View of a task.
    """
    # get date of given task
    task = db_get_task(task_id)
    # if there is no desired task -> 404
    if task is None:
        return abort(404)
    # print task
    return jsonify(task)


def patch_list_id(task_id):
    """
    Executes view handling modifying existing tasks' title, done and done_date
    fields.
    Args:
        task_id (int): Task id.

    Returns:
        Response code successful or failure.
    """
    # get required task
    task = db_get_task(task_id)
    # if task does not exists throw 404 page
    if task is None:
        return abort(404)
    # get data
    data = request.get_json()
    done = data.get('done', None)
    done_date = data.get('done_date', None)
    # if is not given, get the original one
    title = data.get('title', task.get('title'))
    # if nothing was declared, return 204
    if done is None and done_date is None:
        return '', 204
    # need to declare done as it was to detect case
    # (done = None, done_date != None)
    if done is None:
        done = task.get('done')
    # Validate updated data.
    # if task is done and date is not set then set it
    if done and done_date is None:
        done_date = current_date()
    # check if task is not done
    if not done:
        # if task not done and done date is set return 400
        if done_date is not None:
            return abort(400)
        # if not done then set date to null
        else:
            done_date = None
    updated_task = (title, done, done_date, task_id)
    print(updated_task)
    db_update_task(updated_task)
    return '', 204


################################################################################
################################################################################


if __name__ == '__main__':
    if not os.path.exists(DATABASE):
        db_init()
    app.run(debug=True)

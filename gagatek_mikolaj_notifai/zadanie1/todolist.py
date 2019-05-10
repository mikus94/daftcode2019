# coding: utf-8
"""
Zadanie rekrutacyjne Daftcode, Notif.AI.
Zadanie 1.
Autor: Mikolaj Gagatek
email: mikolaj.gagatek@gmail.com
"""

from flask import request, jsonify, abort, Blueprint
import datetime

from .db import *

app_bp = Blueprint('todolist', __name__)


def current_date():
    """
    Obtaining current date and time.
    Returns:
        (str): Current date and time.
    """
    return datetime.datetime.now().replace(microsecond=0)


@app_bp.route('/todolist', methods=['GET', 'POST'])
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
    result = db_get_all_tasks()
    for r in result:
        print(r['created_date'])
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


@app_bp.route('/todolist/<int:task_id>', methods=['PATCH', 'GET', 'DELETE'])
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

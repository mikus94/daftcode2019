import requests
import json
from datetime import datetime


import unittest

SITE = 'http://127.0.0.1:5000/todolist'

# (
#     task,
#     return code,
#     index in db
# )
tasks_post = [
    (
        {
            "title": "Good1",
            "done": False,
            "done_date": None
        },
        200,
        1
    ),
    # bad
    (
        {
            "title": "Bad1",
            "done": False,
            "done_date": "2022-12-12 22:22:22"
        },
        400,
        0
    ),
    (
        {
            "title": "Good 2",
            "done": False
        },
        200,
        2
    ),
    # bad
    (
        {
            "done": False,
        },
        400,
        0
    ),
    (
        {
            "title": "Good 3",
            "done": True
        },
        200,
        3
    ),
    (
        {
            "done_date": "2000-01-01 11-11-11"
        },
        400,
        0
    ),
    (
        {
            "title": "Good 4",
            "done": True,
            "done_date": "2011-11-11 11:11:11"
        },
        200,
        4
    ),
    (
        {
            "title": "Good 5"
        },
        200,
        5
    ),
    # bad
    (
        {
            "title": "Badbbb",
            "done_date": "2022-12-12 22:22:22"
        },
        400,
        0
    )
]

a_ip = '127.0.0.1'
check_init_db = {
    1:  {
            "title": "Good1",
            "done": False,
            "done_date": None,
            "author_ip": a_ip
        },
    2: {
            "title": "Good 2",
            "done": False,
            "done_date": None,
            "author_ip": a_ip
        },
    3:  {
            "title": "Good 3",
            "done": True,
            "author_ip": a_ip
        },
    4:  {
            "title": "Good 4",
            "done": True,
            "done_date": "2011-11-11 11:11:11",
            "author_ip": a_ip
        },
    5:  {
            "title": "Good 5",
            "done": False,
            "done_date": None
        },

}

# database comparator
database = dict()



def init_db():
    for task in tasks_post:
        (j, code, id) = task
        response = requests.post(
            SITE,
            json=j
        )

        if response.status_code != code:
            print("ERRROR!")
            print("INIT!")
            print(task)
            print(response.status_code)
        if response.status_code == 200:
            task_id = response.json()['task_id']
            if task_id != id:
                print("ERROR!")
                print("WRONG ID!")
                print(task)
                print(task_id)
            database[task_id] = j

    print("init ok!")

def list_all():
    response = requests.get(
        SITE
    )
    tasks = response.json()
    for task in tasks:
        tid = task['id']
        tester = check_init_db[tid]
        for field in tester.keys():
            if tester[field] != task[field]:
                print("ERROR!")
                print("list_all")
                print(task)
                print(tester)
    print("list_all OK")

tasks_update = [
    (
        1,
        {
            "title": "foobar",
            "done": True
        },
        {
            "title": "foobar",
            "done": True

        },
        204#code
    ),
    (
        20,
        {},
        {},
        404
    ),
    (
        2,
        {
            "done_date": '2022-12-12 12:12:12'
        },
        {
            "done_date": '2022-12-12 12:12:12'
        },
        400
    ),
    (
        3,
        {
            "title": "barrr2",
            "done_date": '2100-10-10 10:10:10'
        },
        {
            "title": "barrr2",
            "done_date": '2100-10-10 10:10:10'
        },
        204
    )

]

def update():

    now = datetime.now().replace(microsecond=0)
    print(now)


if __name__ == '__main__':
    # init_db()
    list_all()
    update()
    pass

# class TestWWW(unittest.TestCase):
#
#     def initial(self):
#         pass
#     pass
#
#
# if __name__=='__main__':
#     unittest.main()

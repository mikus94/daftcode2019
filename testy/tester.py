import requests
import json

SITE = 'http://127.0.0.1:5000/todolist'


def print_info(resp):
    """
    Printing info.
    Args:
        resp: Response data.
    """

    stuff = [resp.status_code, resp.text, resp.json]
    for s in stuff:
        print(s)

def get_list():
    """
    Main page with list of tasks.
    """
    response = requests.get(SITE)
    print(response.status_code)
    print(response.headers)
    print(response.text)
    print(response.json)

def get_task(id):
    """
    Getting info about 1 task.
    Args:
        id: Id
    """
    response = requests.get(SITE + '/' + str(id))
    print(response.status_code)
    print(response.text)

def post_task():
    """
    Post element from scenario.
    """
    # task to upload
    task = {
        "title": "Conquer the world",
        "done": False,
        "done_date": None
    }
    # post json
    response = requests.post(
        SITE,
        json=task
    )
    # print info about response
    print_info(response)


################################################################################
# /ToDoList
################################################################################

def test_list_bad_post():
    """
    Testing bad posts. Response code should be 400 for all of them.
    """
    tasks = [
        {
            "title": "Bad 1",
            "done": False,
            "done_date": "2099-12-12 12:12:12"
        },
        {
            "title": "Bad 2",
            "done_date": "2099-12-12 12:12:12"
        },
        {
        },
        {
            "done": False
        },
        {
            "done_date": "2099-12-12 12:12:12"
        },
        {
            "done": False,
            "done_date": "2099-12-12 12:12:12"
        }
    ]
    print("Test List Bad Post")
    for task in tasks:
        response = requests.post(
            SITE,
            json=task
        )
        if response.status_code == 400:
            print('OK')
        else:
            print('ERROR')
            print(response.status_code)
            print(task)
    print("//Test Lst Bad Post")


def test_list_good_post():
    """
    Testing good posts.
    Response code should be 200 and returned json with task_id.
    """
    tasks = [
        {
            "title": "Conquer the world",
            "done": False,
            "done_date": None
        },
        {
            "title": "Good 2",
            "done": False
        },

        {
            "title": "Good 3",
            "done": True
        },
        {
            "title": "Good 4",
            "done": True,
            "done_date": "2011-11-11 11:11:11"
        },
        {
            "title": "Good 5"
        }
    ]
    print("Test List Good Post")
    for task in tasks:
        response = requests.post(
            SITE,
            json=task
        )
        title = task['title']
        code = response.status_code
        if code == 200:
            task_id = json.loads(response.text)['task_id']
            print("OK task_id = {}".format(task_id))
        else:
            print("ERROR")
            print(code)
            print(task)
    print("//Test List Good Post")
    pass


def test_good_patch_id():
    """
    Testing bad patching.
    """
    tasks = [
        (
            2,
            {
                "title": "Foobar",
                "done": True
            },
            204
        ),
        (
            2,
            {
                "title": "Learn even more Python",
                "done": False
            },
            204
        ),
        (
            2,
            {
                "done": True,
                "done_date": "2011-11-11 11:11:11"
            },
            204
        ),
        (
            2,
            {
                "done": False,
                "done_date": None
            },
            204
        )
    ]
    print("Test Good Patch Id")
    for (id, task, rcode) in tasks:
        url = SITE + '/' + str(id)
        response = requests.patch(
            url,
            json=task
        )
        if response.status_code == rcode:
            print("OK")
            print(task)
            print("db")
            print(requests.get(url).text)
        else:
            print("ERROR!")
            print(task)
        print("======================================")

    print("//Test Good Patch Id")
    pass

def test_bad_patch_id():
    """
    Testing good patching.
    """
    tasks = [
        (
            999,
            {},
            404
        ),

        (
            1000,
            {
                "title": "CosCos",
                "done": True,
                "done_date": "2099-12-12 12:12:12"
            },
            404
        ),

        (
            2,
            {
                "done": False,
                "done_date": "2011-11-11 11:11:11"
            },
            400
        )
    ]
    print('Test Bad Patch Id')
    for (id, task, rcode) in tasks:
        url = SITE + '/' + str(id)
        response = requests.patch(
            url,
            json=task
        )
        if response.status_code == rcode:
            print("OK")
        else:
            print("ERROR!")
            print(response.status_code)
            print(task)
    print('//Test Bad Patch Id')
    pass

def test_good_delete_id():
    tasks = [
        2,
        6,
        9
    ]
    print("Test Good Delete Id")
    for task in tasks:
        url = SITE + '/' + str(task)
        response = requests.delete(url)
        if response.status_code == 204:
            r2 = requests.get(url)
            if r2.status_code == 404:
                print("OK")
            else:
                print("ERROR!")
                print(task)
        else:
            print("ERROR!")
            print(task)
    print("//Test Good Delete Id")

def test_bad_delete_id():
    tasks = [
        999,
        1000
    ]
    print("Test Bad Delete Id")
    for task in tasks:
        url = SITE + '/' + str(task)
        response = requests.delete(url)
        if response.status_code == 404:
            print("OK")
        else:
            print("ERROR!")
            print(task)
    print("//Test Bad Delete Id")


if __name__ == "__main__":
    post_task()
    test_list_bad_post()
    test_list_good_post()
    test_good_patch_id()
    test_bad_patch_id()
    test_good_delete_id()
    test_bad_delete_id()
    pass

# coding: utf-8
"""
Zadanie rekrutacyjne Daftcode, Notif.AI.
Zadanie 1.
Autor: Mikolaj Gagatek
email: mikolaj.gagatek@gmail.com
"""
import os

from flask import Flask

from . import db
from . import todolist


def create_app():
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        JSONIFY_PRETTYPRINT_REGULAR=True,
        DEBUG=True,
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'database.sqlite'),
    )

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    db.init_app(app)
    app.register_blueprint(todolist.app_bp)
    return app

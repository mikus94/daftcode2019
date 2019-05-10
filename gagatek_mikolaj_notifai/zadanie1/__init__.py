# coding: utf-8
"""
Zadanie rekrutacyjne Daftcode, Notif.AI.
Zadanie 1.
Autor: Mikolaj Gagatek
email: mikolaj.gagatek@gmail.com
"""
import os
from datetime import datetime

from flask import Flask
from flask.json import JSONEncoder


from . import db
from . import todolist


class CustomJSONEncoder(JSONEncoder):
    """
    Custom JSONEncoder to ensure that datetime will be serialized in regular
    string format ('YYYY-MM-DD HH-mm-ss') instead of consistent with RFC 822.
    """
    def default(self, obj):
        try:
            if isinstance(obj, datetime):
                return str(obj)
            iterable = iter(obj)
        except TypeError:
            pass
        else:
            return list(iterable)
        return JSONEncoder.default(self, obj)


def create_app():
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    # assign custom json encoder
    app.json_encoder = CustomJSONEncoder
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

from flask_sqlalchemy import SQLAlchemy
from flask import Flask, jsonify
# from flask_limiter import Limiter
# from flask_limiter.util import get_remote_address

from utils.cfg import DefaultConfig, SqlAlchemyConfig


def create_flask_app_from_obj(config: object):
    sth = Flask(__name__, static_url_path='/s')
    sth.config.from_object(config)
    # app.config.from_pyfile('settings.py')
    # sth.config.from_envvar('FLASK_ENV', silent=True)
    return sth


# app = create_flask_app(DefaultConfig)
app = create_flask_app_from_obj(DefaultConfig)
app.config.from_object(SqlAlchemyConfig)
db = SQLAlchemy(app)


# limiter = Limiter(app=app)
# db = SQLAlchemy()
# db.init_app(app)

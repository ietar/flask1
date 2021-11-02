from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from utils.cfg import SqlAlchemyConfig
db = SQLAlchemy()


class DefaultConfig(object):
    """
    默认配置
    """
    SECRET_KEY = '1dhbuiergv'


def create_flask_app_from_obj(config: object):
    sth = Flask(__name__, static_url_path='/s')
    sth.config.from_object(config)
    # app.config.from_pyfile('settings.py')
    sth.config.from_envvar('FLASK_ENV', silent=True)
    return sth


# app = create_flask_app(DefaultConfig)
app = create_flask_app_from_obj(DefaultConfig)
app.config.from_object(SqlAlchemyConfig)
# db = SQLAlchemy(app)
db.init_app(app)

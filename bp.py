from flask import Flask, Blueprint, g
import json
from goods import goods_bp
from fake_api import fake_api_bp
from utils.cfg import SqlAlchemyConfig
from flask_sqlalchemy import SQLAlchemy


class DefaultConfig(object):
    """
    默认配置
    """
    SECRET_KEY = '1dhbuiergv'


class DevConfig(DefaultConfig):
    DEBUG = True
    # FLASK_ENV = 'development'
    # FLASK_ENV = 'production'


def create_flask_app(config: object):

    sth = Flask(__name__, static_url_path='/s')
    sth.config.from_object(config)
    # app.config.from_pyfile('settings.py')
    sth.config.from_envvar('FLASK_ENV', silent=True)
    return sth


# app = create_flask_app(DefaultConfig)
app = create_flask_app(DevConfig)
app.config.from_object(SqlAlchemyConfig)
user_bp = Blueprint('user', __name__)


@user_bp.route('/profile', methods=['post', 'get'])
def get_profile():

    return 'user profile'


@app.route('/')
def index():
    return 'this is a flask app'


app.register_blueprint(user_bp, url_prefix='/user')
app.register_blueprint(goods_bp, url_prefix='/goods')
app.register_blueprint(fake_api_bp, url_prefix='/fake_api')
db = SQLAlchemy(app)
# db = SQLAlchemy(app)
# g.db = db


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)

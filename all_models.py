# from flask import Flask, current_app
# from flask_sqlalchemy import SQLAlchemy
# from utils.cfg import SqlAlchemyConfig
from flask_migrate import Migrate
import datetime
from exts import app, db
# from begin import app

# app = Flask(__name__)
# app.config.from_object(SqlAlchemyConfig)
# db = SQLAlchemy(app)
migrate = Migrate(app, db, compare_type=True, compare_server_default=True)
environment = {'wsgi.vresion': (1, 0), 'wsgi.input': '', 'REQUEST_METHOD': 'GET', 'PATH_INFO': '/',
               'SERVER_NAME': 'ietar_server', 'wsgi.url_scheme': "http", 'SERVER_HOST': '80'}


class User1(db.Model):

    class Status(object):
        Disable = 0
        able = 1

    __tablename__ = 'user_basic'

    user_id = db.Column('user_id', db.Integer, primary_key=True)
    account = db.Column(db.String(64), unique=True, nullable=False)  # 用户名
    nickname = db.Column(db.String(16), default='')
    password = db.Column(db.String(64), nullable=False)
    email = db.Column(db.String(64), default='')
    status = db.Column(db.SmallInteger, default=1)
    salt = db.Column(db.String(64), nullable=False, default='')
    token = db.Column(db.String(128), nullable=True)
    token_expire = db.Column(db.DateTime, nullable=True, default=datetime.datetime.now())


class User2(db.Model):

    class Status(object):
        Disable = 0
        able = 1

    __tablename__ = 'user_basic_2'

    user_id = db.Column('user_id', db.Integer, primary_key=True)
    account = db.Column(db.String(64))
    email = db.Column(db.String(64))
    status = db.Column(db.SmallInteger, default=1)
    gender = db.Column(db.Boolean, default=1)


class User3(db.Model):

    class Status(object):
        Disable = 0
        able = 1

    __tablename__ = 'user_basic_3'

    user_id = db.Column('user_id', db.Integer, primary_key=True)
    account = db.Column(db.String(16))
    email = db.Column(db.String(16))
    status = db.Column(db.SmallInteger, default=1)

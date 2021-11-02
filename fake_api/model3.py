from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from utils.cfg import SqlAlchemyConfig
from flask_migrate import Migrate


app = Flask(__name__)
app.config.from_object(SqlAlchemyConfig)
db = SQLAlchemy(app)
migrate = Migrate(app, db, compare_type=True, )


class User3(db.Model):

    class Status(object):
        Disable = 0
        able = 1

    __table_name__ = 'user_basic_3'

    user_id = db.Column('user_id', db.Integer, primary_key=True)
    account = db.Column(db.String(16))
    email = db.Column(db.String(16))
    status = db.Column(db.SmallInteger, default=1)

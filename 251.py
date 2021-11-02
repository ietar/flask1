from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from fake_api import fake_api_bp
from utils.cfg import SqlAlchemyConfig


app = Flask(__name__)
app.config.from_object(SqlAlchemyConfig)
db = SQLAlchemy(app)
app.register_blueprint(fake_api_bp, prefix_url='fake_api')


# class User1(db.Model):
#
#     class Status(object):
#         Disable = 0
#         able = 1
#
#     __table_name = 'user_basic'
#
#     user_id = db.Column('user_id', db.Integer, primary_key=True)
#     account = db.Column(db.String)
#     email = db.Column(db.String)
#     status = db.Column(db.SmallInteger, default=1)


@app.route('/')
def index():
    return f'index'


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)

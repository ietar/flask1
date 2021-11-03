from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
# from first import models # 模型文件必须导入进来，否则运行报错


class Config(object):
    SQLALCHEMY_DATABASE_URI = "mysql://flask:123456@127.0.0.1:3306/flask_db_1"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMYECHO = True


app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)


class User1(db.Model):

    class Status(object):
        Disable = 0
        able = 1

    __table_name = 'user_basic'

    user_id = db.Column('user_id', db.Integer, primary_key=True)
    account = db.Column(db.String(64))
    email = db.Column(db.String(64))
    status = db.Column(db.SmallInteger, default=1)
    gender = db.Column(db.Boolean, default=1)


migrate = Migrate(app=app, db=db)
# manager.add_command('start', Server(port=8000, use_debugger=True))  # 创建启动命令

# if __name__ == '__main__':
#     app.run()

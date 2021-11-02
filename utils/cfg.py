class SqlAlchemyConfig(object):
    SQLALCHEMY_DATABASE_URI = "mysql://flask:123456@127.0.0.1:3306/flask_db_1"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = True

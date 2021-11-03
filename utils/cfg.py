class SqlAlchemyConfig(object):
    SQLALCHEMY_DATABASE_URI = "mysql://flask:123456@127.0.0.1:3306/flask_db_1"  # user:flask pw:123456 db:flask_db_1
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = True


class DefaultConfig(object):
    """
    默认配置
    """
    SECRET_KEY = '1dhbuiergv'
    USER_TOKEN_EXPIRE = 3600 * 24
    # DEBUG = False
    DEBUG = True

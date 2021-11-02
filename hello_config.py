from flask import Flask
import json


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


@app.route('/')
def index():
    # s = 'hello'
    # s1 = app.config.get('ENV')
    # s += s1
    # # for k, v in app.config.items():
    # #     print(k, v)
    # # print('ietar running mode:', s1)
    # return s
    rules_iterator = app.url_map.iter_rules()
    res = {rule.endpoint: rule.rule for rule in rules_iterator}
    print(res)
    return json.dumps(res)


if __name__ == '__main__':
    app.run(port=8000)

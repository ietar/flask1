from flask import Flask, request, render_template, jsonify, redirect, make_response, session, abort
from werkzeug.routing import BaseConverter
from goods import goods_bp


class FlaskConfig(object):
    SECRET_KEY = 'i1hdug3u'


app = Flask(__name__)
app.config.from_object(FlaskConfig)
app.redis_port = '6379'
app.register_blueprint(goods_bp, url_prefix='/goods')


@app.route('/')
def index():
    return 'index'


@app.before_first_request
def before_1():
    return print('before_1')


@app.before_request
def before_r():
    return print('before_r')


@app.after_request
def after_r(resp):
    resp.data += b'<br>after_request'
    print('after_r')
    return resp


@app.teardown_request
def teardown_r(e):
    print(e)
    print('teardown_r')
    # resp.data += b'<br>teardown_r'
    # resp.data += f'<br>{str(error)}'.encode()
    # return resp


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)

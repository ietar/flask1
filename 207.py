from flask import Flask, request, render_template, jsonify, redirect, make_response, session, abort
from werkzeug.routing import BaseConverter


class FlaskConfig(object):
    SECRET_KEY = 'i1hdug3u'


app = Flask(__name__)
app.config.from_object(FlaskConfig)


@app.route('/sessions', methods=['get'])
def sessions():
    res = make_response('sessions:')
    # res.data += b'hello'
    uname = session.get('uname')
    res.data += uname.encode()
    # session['uname'] = 'session_name'
    return res


@app.route('/dont_touch_me_500', methods=['get'])
def dont_touch_me_500():
    abort(500)
    return None


@app.route('/dont_touch_me_0', methods=['get'])
def dont_touch_me_0():

    return 1/0


@app.errorhandler(500)
def status_500(error, *args, **kwargs):
    # print('args:', args)
    # print('kwargs:', kwargs)
    return f'the error is: {error}<br>heyhey 500'


@app.errorhandler(ZeroDivisionError)
def zero_division(error, *args, **kwargs):
    # print('args:', args)
    # print('kwargs:', kwargs)

    return f'the error is: {error}<br>heyhey 500', 500, {}


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)

from flask import Flask, request, render_template, jsonify, redirect, make_response, session, abort, g
from werkzeug.routing import BaseConverter
from goods import goods_bp

app = Flask(__name__)


@app.before_request
def au():
    # g.user_id = 123
    g.user_id = None
    pass


# decorator
def login_required(func):
    def wrapper(*args, **kwargs):
        if g.user_id is None:
            abort(401)
        else:
            return func(*args, **kwargs)
    return wrapper


@app.route('/')
@login_required
def index():
    return f'user_id = {g.user_id}'


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)

from flask import Flask, request, render_template, jsonify, redirect, make_response, session, abort, g
from flask_restful import Resource, Api
from goods import goods_bp
from utils.decorators import deco1, deco2

app = Flask(__name__)
api = Api(app)


class HelloWorldResource(Resource):

    method_decorators = [deco1, deco2]

    def get(self):
        return {'hello': 'world'}

    def post(self):
        return {'msg': 'post hello world'}

    def delete(self):
        return jsonify({'msg': 'delete hello world'})


api.add_resource(HelloWorldResource, r'/re')
app.register_blueprint(goods_bp, url_prefix=r'/goods')


@app.route('/')
def index():
    g.user_id = 4
    return f'user_id = {g.user_id}'


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)

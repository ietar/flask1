# from . import goods_bp
from flask import Blueprint, current_app
from flask_restful import Api, Resource, reqparse
from utils.decorators import deco1, deco2
import flask_restful.inputs as fri
import re


def mobile(mobile_str):
    mobile_str = str(mobile_str)
    p = r'\d{11}'
    pattern = re.compile(p)
    if pattern.fullmatch(mobile_str):
        return mobile_str
    else:
        raise TypeError(f"pattern {p} doesn't match")


goods_bp = Blueprint('goods', __name__, static_url_path='/s', static_folder='static')
parser = reqparse.RequestParser()
parser.add_argument('name', required=True, location=['json', 'form'])
parser.add_argument('color', action='append')
parser.add_argument(name='feet', type=int, help='feet int', location='args')
parser.add_argument('url', type=fri.url)
parser.add_argument(r're4', action=fri.regex(r'\d{4}'))
parser.add_argument('range5', type=fri.int_range(0, 5))
parser.add_argument('bool', type=fri.boolean)
# parser.add_argument('mo', type=mobile, location='form')
parser.add_argument('mo', type=mobile, location='json')


@goods_bp.route('/profile')
def get_goods():
    return 'get goods1'


@goods_bp.route('/<int:good_id>')
def get_good(good_id):
    t = type(good_id)
    r = f'get good by good_id:{good_id}\ntype: {t}'
    print(r)
    print(t)
    return r


@goods_bp.route('/redis_port')
def redis_port():
    return current_app.redis_port


class JuiceResource(Resource):

    method_decorators = {'get': [deco1], 'post': [deco2, deco1]}

    def get(self):
        args = parser.parse_args()
        res = {k: v for k, v in args.items() if v}
        # res = {
        #     'where am i': 'get juice',
        #     'fruit_name': args.get('name'),
        #     'color': args.get('color'),
        #     'feet': args.get('feet')
        # }
        return res

    def post(self):
        args = parser.parse_args()
        res = {k: v for k, v in args.items() if v}
        # res = {
        #     'where am i': 'get juice',
        #     'fruit_name': args.get('name'),
        #     'color': args.get('color'),
        #     'feet': args.get('feet')
        # }
        return res

    def put(self):
        args = parser.parse_args()
        res = {k: v for k, v in args.items() if v}
        # res = {
        #     'where am i': 'get juice',
        #     'fruit_name': args.get('name'),
        #     'color': args.get('color'),
        #     'feet': args.get('feet')
        # }
        return res


api = Api(goods_bp)
api.add_resource(JuiceResource, '/juice')


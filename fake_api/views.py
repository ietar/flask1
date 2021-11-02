# from . import goods_bp
from flask import Blueprint, jsonify
from flask_restful import Api, Resource
# from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import load_only
import re
import time

from exts import db
from all_models import User1
from utils.tools import mk_salt, mk_pw
from utils.parsers import get_user_parser, register_post_parser, text_parser, token_parser
from utils.decorators import deco1, deco2


def mobile(mobile_str):
    mobile_str = str(mobile_str)
    p = r'\d{11}'
    pattern = re.compile(p)
    if pattern.fullmatch(mobile_str):
        return mobile_str
    else:
        raise TypeError(f"pattern {p} doesn't match")


fake_api_bp = Blueprint('fake_api', __name__, static_url_path='/s', static_folder='static')


class JuiceResource(Resource):

    method_decorators = {'get': [deco1], 'post': [deco2, deco1]}

    def get(self):
        args = text_parser.parse_args()
        res = {k: v for k, v in args.items() if v}
        # res = {
        #     'where am i': 'get juice',
        #     'fruit_name': args.get('name'),
        #     'color': args.get('color'),
        #     'feet': args.get('feet')
        # }
        return res

    def post(self):
        args = text_parser.parse_args()
        res = {k: v for k, v in args.items() if v}
        # res = {
        #     'where am i': 'get juice',
        #     'fruit_name': args.get('name'),
        #     'color': args.get('color'),
        #     'feet': args.get('feet')
        # }
        return res

    def put(self):
        args = text_parser.parse_args()
        res = {k: v for k, v in args.items() if v}
        # res = {
        #     'where am i': 'get juice',
        #     'fruit_name': args.get('name'),
        #     'color': args.get('color'),
        #     'feet': args.get('feet')
        # }
        return res


class UserResource(Resource):

    def get(self):
        """
        获取用户信息
        todo 传入token获取额外私人信息
        :return:
        """
        res = {'status': True, 'msg': '', 'data': {}}
        try:
            account = get_user_parser.parse_args().get('account')
            users = User1.query.filter_by(account=account)
            user1 = users.first()
            if user1 is None:
                res['status'] = False
                res['data'] = f"can not get user by account {account}"
                return jsonify(res)

            append = {'user_id': user1.user_id,
                      'account': user1.account,
                      'nickname': user1.nickname,
                      'email': user1.email,
                      'status': user1.status}
            res['data'].update(append)
        except Exception as e:
            res['status'] = False
            res['msg'] = str(e)
        return jsonify(res)

    def post(self):
        res = {'status': True, 'msg': '', 'data': {}}
        try:
            args = register_post_parser.parse_args()
            # print(args)
            account = args.get('account')
            password = args.get('password')
            email = args.get('email', '')
            nickname = args.get('nickname', '')

            users = User1.query.options(load_only(User1.account)).all()
            user_account_list = [user.account for user in users]
            if account in user_account_list:
                res['status'] = False
                res['msg'] = f'account {account} already exists'
                return jsonify(res)

            salt = mk_salt()
            encrypted_password = mk_pw(pw=password, salt=salt)

            new_user = User1(account=account, email=email, nickname=nickname, password=encrypted_password, salt=salt)
            db.session.add(new_user)
            # db.session.add_all([new_user, new_user2])
            db.session.commit()

            append = {'user_id': new_user.user_id,
                      'account': new_user.account,
                      'nickname': new_user.nickname,
                      'email': new_user.email,
                      'status': new_user.status}
            res['data'].update(append)
        except Exception as e:
            res['status'] = False
            res['msg'] = str(e)
        # print(res)
        return jsonify(res)

    def delete(self):
        res = {'status': True, 'msg': '', 'data': {}}
        try:
            args = token_parser.parse_args()
            user_id = args.get('id')
            token = args.get('token')
            if token is None:
                res['status'] = False
                res['msg'] = f'param "token" required'
                return jsonify(res)

            user1 = User1.query.filter_by(user_id=user_id).first()
            if user1 is None:
                res['status'] = False
                res['msg'] = f'user_id {user_id} does not exists'
                return jsonify(res)

            db.session.delete(user1)
            db.session.commit()
            res['msg'] = f'delete account {user1.account}'
            return jsonify(res)

        except Exception as e:
            res['status'] = False
            res['data'] = str(e)
        return jsonify(res)


class UserTokenResource(Resource):

    def post(self):
        res = {'status': True, 'msg': '', 'data': {}}
        args = token_parser.parse_args()
        user_id = args.get('id')
        pw = args.get('pw')
        refresh = args.get('refresh')
        # print(args)

        user = User1.query.filter_by(user_id=user_id).first()
        if user is None:
            res['status'] = False
            res['data'] = f"can not get user by user_id {id}"
            return jsonify(res)

        salt = user.salt
        e_pw = mk_pw(pw=pw, salt=salt)
        e_pw_db = user.password
        if e_pw != e_pw_db:
            res['status'] = False
            res['data'] = f"password not matched {pw}"
            # print(e_pw, e_pw_db)
            return jsonify(res)

        # 直接生成个新的
        if refresh or (user.token is None):
            token = mk_pw(pw=str(time.time()), salt=mk_salt())
            user.token = token
            db.session.add(user)
            db.session.commit()
        else:
            token = user.token

        res['data'].update({
            'token': token
        })
        return jsonify(res)


api = Api(fake_api_bp)
api.add_resource(JuiceResource, r'/juice')
api.add_resource(UserResource, r'/user')
api.add_resource(UserTokenResource, r'/user/token')

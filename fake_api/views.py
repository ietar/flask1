# -*- coding: utf-8 -*-

# from . import goods_bp
from flask import Blueprint, jsonify, current_app, make_response
from flask_restful import Api, Resource
# from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import load_only, contains_eager
# from sqlalchemy import or_, and_, not_, func
import time
import datetime
# import traceback
from flask_limiter import Limiter, HEADERS
from flask_limiter.util import get_remote_address


from exts import db, app
from all_models import User1, Comment
from utils.tools import mk_salt, mk_pw
from utils.parsers import get_user_parser, register_post_parser, text_parser, token_parser, comment_parser
from utils.decorators import deco1, deco2
from utils.ietar_limit import Limiter1


fake_api_bp = Blueprint('fake_api', __name__, static_url_path='/s', static_folder='static')
limiter = Limiter(app, key_func=get_remote_address, headers_enabled=True, storage_uri=app.config.get('REDIS_URI'))
#  storage_uri 需要手动安装 pip install flask-redis
limiter.header_mapping = {
    HEADERS.LIMIT: 'X-My-Limit',
    HEADERS.RESET: "X-My-Reset",
    HEADERS.REMAINING: "X-My-Remaining"}
# or by only partially specifying the overrides

limiter1 = Limiter1(app)


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

    # method_decorators = {
    #     'get': [limiter.limit('1/day'), ],
    #     'post': [limiter.limit('2/day')]
    # }
    # method_decorators = [limiter.limit('1/day')]

    # decorators = [limiter.limit('5/minute')]  # CBV只能用这个

    @limiter1.limit(amount=5, many_interval=1, interval='min')
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
                res['msg'] = f"can not get user by account {account}"
                return make_response(jsonify(res))

            append = {'user_id': user1.user_id,
                      'account': user1.account,
                      'nickname': user1.nickname,
                      'email': user1.email,
                      'status': user1.status}
            res['data'].update(append)
        except Exception as e:
            # print(traceback.format_exc())
            # print(type(e))
            res['status'] = False
            res['msg'] = str(e)
            return make_response(jsonify(res), 500)
        return make_response(jsonify(res))

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
                return make_response(jsonify(res), 400)

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
            return make_response(jsonify(res), 500)
        # print(res)
        return make_response(jsonify(res))

    def delete(self):
        res = {'status': True, 'msg': '', 'data': {}}
        try:
            args = token_parser.parse_args()
            user_id = args.get('id')
            token = args.get('token')
            if token is None:
                res['status'] = False
                res['msg'] = f'param "token" required'
                return make_response(jsonify(res), 400)

            user1 = User1.query.filter_by(user_id=user_id).first()
            if user1 is None:
                res['status'] = False
                res['msg'] = f'user_id {user_id} does not exists'
                return make_response(jsonify(res))

            if user1.token != token:
                res['status'] = False
                res['msg'] = f'invalid token'
                return make_response(jsonify(res), 401)

            db.session.delete(user1)
            db.session.commit()
            res['msg'] = f'delete account {user1.account}'

        except Exception as e:
            res['status'] = False
            res['data'] = str(e)
            return make_response(jsonify(res), 500)
        return make_response(jsonify(res))


# @limiter.limit(limit_value='1 per day')
class UserTokenResource(Resource):

    def get(self):
        # for test
        # users = User1.query.options(load_only(User1.user_id, User1.account)) \
        #     .filter(User1.user_id % 2, User1.account.startswith('ie')).all()
        # users = User1.query.options(load_only(User1.user_id, User1.account)) \
        #     .filter(or_(User1.user_id % 2, User1.account.startswith('ie'))).all()
        # users = User1.query.options(load_only(User1.user_id, User1.account)).offset(3).all()
        # users = User1.query.options(load_only(User1.user_id, User1.account)).order_by(User1.user_id.desc())
        # 聚合
        # users = db.session.query(User1.user_id, User1.nickname, func.count(User1.nickname))
        # .group_by(User1.nickname).all()

        # join important
        # join important
        # r = Comment.query.join(Comment.user)\
        #     .options(load_only(Comment.user_id, Comment.comment_id),
        #              contains_eager(Comment.user).load_only(User1.account))\
        #     .filter(Comment.user_id == 13).all()
        # print(r[0].user[0].account)

        user = User1.query.options(load_only(User1.user_id)).get(13)
        # print('here:', user.comment)
        temp = []
        for c in user.comment:
            temp.append({
                'comment_id': c.comment_id,
                'user_id': c.user_id,
                'comment': c.comment,
                'ts': c.ts
            })
        return jsonify(temp)

        # res = {'status': True, 'msg': '', 'data': {}}
        # res = {'status': True, 'msg': '', 'data': []}
        # for u in users:
        #     # res['data'].update({
        #     #     'user_id': u.user_id,
        #     #     'account': u.account
        #     # })
        #     res['data'].append({
        #         'user_id': u.user_id,
        #         'account': u.account
        #     })
        # return make_response(jsonify(res))

    def post(self):
        res = {'status': True, 'msg': '', 'data': {}}
        args = token_parser.parse_args()
        user_id = args.get('user_id')
        pw = args.get('pw')
        refresh = args.get('refresh')
        # print(args)

        user = User1.query.filter_by(user_id=user_id).first()
        if user is None:
            res['status'] = False
            res['data'] = f"can not get user by user_id:{user_id}"
            return make_response(jsonify(res))

        salt = user.salt
        e_pw = mk_pw(pw=pw, salt=salt)
        e_pw_db = user.password
        if e_pw != e_pw_db:
            res['status'] = False
            res['data'] = f"password not matched {pw}"
            # print(e_pw, e_pw_db)
            return make_response(jsonify(res), 401)

        # 直接生成个新的
        if refresh or (user.token is None):
            token = mk_pw(pw=str(time.time()), salt=mk_salt())
            user.token = token
            expire_offset = datetime.timedelta(seconds=int(current_app.config.get('USER_TOKEN_EXPIRE')))
            user.token_expire = datetime.datetime.utcnow() + expire_offset
            db.session.add(user)
            db.session.commit()
            res['data'].update({'expire': user.token_expire})
        else:
            token = user.token

        res['data'].update({
            'token': token
        })
        return make_response(jsonify(res))


class CommentResource(Resource):

    def get(self):
        """
        优先comment_id 若无该参数则按user_id查询
        :return:
        """
        res = {'status': True, 'msg': '', 'data': []}
        try:
            args = comment_parser.parse_args()
            comment_id = args.get('comment_id')
            user_id = args.get('user_id')

            if comment_id:
                comment = Comment.query.get(comment_id)
                if not comment:
                    res['status'] = False
                    res['msg'] = f"can not get comment by comment_id {comment_id}"
                    return make_response(jsonify(res))

                res['data'].append({
                    'comment_id': comment.comment_id,
                    'user_id': comment.user_id,
                    'comment': comment.comment,
                    'ts': comment.ts,
                })

            elif user_id:
                comments = Comment.query.filter_by(user_id=user_id).all()
                for i in comments:
                    res['data'].append({
                        'comment_id': i.comment_id,
                        'user_id': i.user_id,
                        'comment': i.comment,
                        'ts': i.ts,
                    })
            else:
                res['status'] = False
                res['msg'] = 'either comment_id or user_id required'

        except Exception as e:
            res['status'] = False
            res['msg'] = str(e)
        return make_response(jsonify(res))

    def post(self):
        res = {'status': True, 'msg': '', 'data': {}}
        try:
            args = comment_parser.parse_args()
            user_id = args.get('user_id')
            token = args.get('token')
            comment = args.get('comment')

            user = User1.query.filter(User1.user_id == user_id).first()
            if not user:
                res['status'] = False
                res['msg'] = f"can not get user by user_id {user_id}"
                return make_response(jsonify(res))

            if token != user.token:
                res['status'] = False
                res['msg'] = f"token invalid"
                return make_response(jsonify(res))

            utc_now = datetime.datetime.utcnow()
            if user.token_expire < utc_now:
                res['status'] = False
                res['msg'] = f"token expired. " \
                    f"post /fake_api/user/token with param id(user_id),pw(password),refresh=1 " \
                    f"to get a fresh token"
                return make_response(jsonify(res))

            new_comment = Comment(user_id=user_id, comment=comment, ts=datetime.datetime.utcnow())
            db.session.add(new_comment)
            db.session.commit()
            res['msg'] = 'add comment successfully'
        except Exception as e:
            res['status'] = False
            res['msg'] = str(e)
        return make_response(jsonify(res))


api = Api(fake_api_bp)
api.add_resource(JuiceResource, r'/juice')
api.add_resource(UserResource, r'/user')
api.add_resource(UserTokenResource, r'/user/token')
api.add_resource(CommentResource, r'/comment')


@fake_api_bp.route(r'/')
@limiter.limit('1/day')
def fake():
    return '121'


# @app.route('/221', methods=['post'])
# def p221():
#     return 'p221'

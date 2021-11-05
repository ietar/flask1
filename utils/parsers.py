from flask_restful import reqparse
import flask_restful.inputs as fri
import re


# user get用parser
get_user_parser = reqparse.RequestParser()
get_user_parser.add_argument('account', required=True)
get_user_parser.add_argument('token')


# 注册post用parser
register_post_parser = reqparse.RequestParser()
register_post_parser.add_argument('account', location='form', nullable=False)
register_post_parser.add_argument('password', location='form', nullable=False)
register_post_parser.add_argument('email', location='form')
register_post_parser.add_argument('nickname', location='form')

# test用parser
text_parser = reqparse.RequestParser()
text_parser.add_argument('name', required=True, location=['json', 'form'])
text_parser.add_argument('color', action='append')
text_parser.add_argument(name='feet', type=int, help='feet int', location='args')
text_parser.add_argument('url', type=fri.url)
text_parser.add_argument(r're4', action=fri.regex(r'\d{4}'))
text_parser.add_argument('range5', type=fri.int_range(0, 5))
text_parser.add_argument('bool', type=fri.boolean)
# parser.add_argument('mo', type=mobile, location='form')
# text_parser.add_argument('mo', type=mobile, location='json')

# token用parser
token_parser = reqparse.RequestParser()
token_parser.add_argument('user_id', location='form', nullable=False)
token_parser.add_argument('pw', location='form', nullable=False)
token_parser.add_argument('refresh', type=fri.boolean)  # 1 刷新 0 不刷新
token_parser.add_argument('token', location='form')


def mobile(mobile_str):
    mobile_str = str(mobile_str)
    p = r'\d{11}'
    pattern = re.compile(p)
    if pattern.fullmatch(mobile_str):
        return mobile_str
    else:
        raise TypeError(f"pattern {p} doesn't match")


comment_parser = reqparse.RequestParser()
comment_parser.add_argument('comment_id')
comment_parser.add_argument('user_id')
comment_parser.add_argument('comment')
comment_parser.add_argument('token')


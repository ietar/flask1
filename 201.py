from flask import Flask, request, render_template, jsonify, redirect, make_response
from werkzeug.routing import BaseConverter


class MobileConverter(BaseConverter):
    regex = r'1[3-9]\d{9}'


app = Flask(__name__, template_folder='templates')
app.url_map.converters['mobile'] = MobileConverter


@app.route('/<mobile:mobile_num>')
def mob(mobile_num):
    r = mobile_num
    print(type(r))
    return r


@app.route('/')
def index():
    # r = 'index here'
    data = {
        'my_str': 'ietar',
        'my_int': 121,
    }
    return render_template(r'index.html', **data)


# /book?id=3
@app.route('/book')
def book():
    _id = request.args.get('id')
    print(type(_id))
    r = f'book_id = {_id}'
    return r


@app.route('/post_file', methods=['post'])
def post_file():
    file = request.files['f']
    filename = request.args.get('filename')
    print(file, filename)
    r = f'name: {filename} content_length:{request.content_length}'
    # file.save(filename)
    return r


@app.route('/r1', methods=['get'])
def r1():
    return redirect('/')


@app.route('/jsf', methods=['get'])
def jsf():
    return jsonify({'name': 'ietar'})


@app.route('/tuple_res', methods=['get'])
def tuple_res():
    """
    401 unauthorized
    :return:
    """
    return 'aoe_eof', 401, {'locations': 'hell', 'ts': 1024}


@app.route('/mk_res', methods=['get'])
def mk_res():
    """
    402 payment required
    :return:
    """

    res = make_response('aoe_eof_make_response')
    # res.status_code = 402
    res.status = '403 whatever'
    res.headers['location'] = 'mk_res'
    return res


@app.route('/set_cookie', methods=['get'])
def set_cookie():
    res = make_response('aoe_eof_make_response')
    res.status_code = 200
    res.set_cookie('name', 'flask1_cookie')
    res.set_cookie('expire', 'flask1_cookie_3600', max_age=3600)
    return res


@app.route('/get_del_cookie', methods=['get'])
def get_del_cookie():
    res = make_response('get_del_cookie')
    # res.status_code = 200
    name = request.cookies.get('name')
    # print(name)
    # print(res.data, type(res.data))
    res.data += b'hello'
    res.delete_cookie('name')
    return res


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)

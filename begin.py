from flask import Flask, Blueprint, g
from goods import goods_bp
from exts import app
# from utils.cfg import SqlAlchemyConfig
from fake_api.views import fake_api_bp

from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

lt = Limiter(app, key_func=get_remote_address)

@app.route('/')
@lt.limit('1/day')
def index():
    return 'this is a flask app'


app.register_blueprint(goods_bp, url_prefix='/goods')
app.register_blueprint(fake_api_bp, url_prefix='/fake_api')

if __name__ == '__main__':

    app.run(host='0.0.0.0', port=8000)

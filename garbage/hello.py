from flask import Flask


app = Flask(__name__, static_url_path='/s')


@app.route('/')
def index():
    return 'hello'

#
# if __name__ == '__main__':
#     app.run()

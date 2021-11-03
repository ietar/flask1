from flask import Flask

# app = Flask(__name__)
app = Flask(__name__, static_url_path='/s')
app.config.from_envvar()


@app.route('/')
def index():
    return 'hello world'


if __name__ == '__main__':
    app.run()

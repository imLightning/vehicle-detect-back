from flask import Flask
from flask_cors import cross_origin
from apps.login import to_login
from apps.register import to_register

app = Flask(__name__, static_folder='static')


@app.route('/register', methods=['GET', 'POST'])
#注册
def on_register():
    return to_register()


@app.route('/login', methods=['GET', 'POST'])
#登录
def on_login():
    return to_login()


@app.route('/')
@cross_origin(origins='http://localhost:8080')
def hello_world():  # put application's code here
    return 'Hello World!'

if __name__ == '__main__':
    app.run()

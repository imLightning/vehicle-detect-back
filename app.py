from flask import Flask
from flask_cors import cross_origin

app = Flask(__name__, static_folder='static')

@app.route('/')
@cross_origin(origins='http://localhost:8080')
def hello_world():  # put application's code here
    return 'Hello World!'

if __name__ == '__main__':
    app.run()

from flask import Flask, request
from flask_cors import cross_origin
from apps.file.upload import upload
from apps.detect import vehicle as ve
from utils.result import Result
from utils import recept
from apps.login import to_login
from apps.register import to_register

SPEED_LIMIT = 140

app = Flask(__name__, static_folder='static')


@app.route('/register', methods=['GET', 'POST'])
#注册
def on_register():
    return to_register()

@app.route('/login', methods=['GET', 'POST'])
#登录
def on_login():
    return to_login()

# 录像上传函数
@app.route('/recordUpload', methods=['POST'])
@cross_origin(origins='http://localhost:8080')
def record_upload():  # put application's code here
    return upload()

# 设置
@app.route('/setting/get', methods=['GET'])
@cross_origin(origins='http://localhost:8080')
def get_setting():
    return Result.success({
        "SPEED_LIMIT": SPEED_LIMIT,
    })

@app.route('/setting/update', methods=['POST'])
@cross_origin(origins='http://localhost:8080')
def update_setting():
    data = recept.to_dict(request.data)
    global SPEED_LIMIT
    SPEED_LIMIT = data['SPEED_LIMIT']
    return Result.success()

def detect_process():
    print("======START DETECTION======")
    ve.vehicle_detect()
    print("======END   DETECTION======")
    return True

if __name__ == '__main__':
    app.run()

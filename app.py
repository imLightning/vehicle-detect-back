from flask import Flask, request
from flask_cors import cross_origin

from detect import vehicle as ve
from threading import Thread
from utils import result

SPEED_LIMIT = 140

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

# 录像上传函数
@app.route('/recordUpload', methods=['POST'])
@cross_origin(origins='http://localhost:8080')
def record_upload():  # put application's code here
    record = request.files['record']
    # 文件写入磁盘
    record.save('./file/records/' + record.filename)
    # 记录数据库
    # 建立线程车辆检测
    t=Thread(target=detect_process)
    t.start()
    return result.ok()

# 设置
@app.route('/setting/get', methods=['GET'])
@cross_origin(origins='http://localhost:8080')
def get_setting():
    return result.ok({
        "SPEED_LIMIT": SPEED_LIMIT,
    })

@app.route('/setting/update', methods=['POST'])
@cross_origin(origins='http://localhost:8080')
def update_setting():
    data = dict(request.data)
    global SPEED_LIMIT
    SPEED_LIMIT = data['SPEED_LIMIT']
    return result.ok()

def detect_process():
    print("======START DETECTION======")
    ve.vehicle_detect()
    print("======END   DETECTION======")
    return True

if __name__ == '__main__':
    app.run()

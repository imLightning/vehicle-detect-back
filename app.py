from flask import Flask, request
from flask_cors import cross_origin
from apps.detect.process import detect_file
from apps.file.download import get_res
from apps.file.upload import upload, get_file, manual_upload, del_file, del_res
from apps.detect import vehicle as ve
from utils.result import Result
from utils import recept
from apps.detect import vehicle as ve
from apps.login import to_login, is_login

SPEED_LIMIT = 140

app = Flask(__name__, static_folder='static')


@app.route('/login', methods=['GET', 'POST'])
@cross_origin(origins='http://localhost:8080')
#登录
def on_login():
    return to_login()

@app.route('/is_login/<token>', methods=['GET', 'POST'])
@cross_origin(origins='http://localhost:8080')
#登录
def logined(token):
    return is_login(token)


@app.route('/')
@cross_origin(origins='http://localhost:8080')
def hello_world():  # put application's code here
    return 'Hello World!'


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
    data = recept.to_dict()
    global SPEED_LIMIT
    SPEED_LIMIT = data['SPEED_LIMIT']
    return Result.success()

def detect_process():
    print("======START DETECTION======")
    ve.vehicle_detect()
    print("======END   DETECTION======")
    return True

@app.route('/file/get', methods=['GET'])
@cross_origin(origins='http://localhost:8080')
def get_allfile():  # put application's code here
    return get_file()

@app.route('/file/detect', methods=['POST'])
@cross_origin(origins='http://localhost:8080')
def record_detect():  # put application's code here
    return detect_file()

@app.route('/res/get', methods=['GET'])
@cross_origin(origins='http://localhost:8080')
def get_allres():  # put application's code here
    return get_res()

@app.route('/upload', methods=['POST'])
@cross_origin(origins='http://localhost:8080')
def com_upload():
    return manual_upload()

@app.route('/file/delete', methods=['POST'])
@cross_origin(origins='http://localhost:8080')
def record_delete():
    return del_file()

@app.route('/res/delete', methods=['POST'])
@cross_origin(origins='http://localhost:8080')
def res_delete():
    return del_res()

if __name__ == '__main__':
    app.run()

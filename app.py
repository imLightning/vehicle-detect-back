from flask import Flask, request
from flask_cors import cross_origin
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
from detect import vehicle as ve
from threading import Thread
from global_handle import result, reception
import time

SPEED_LIMIT = 140

app = Flask(__name__, static_folder='static')

HOSTNAME = "127.0.0.1"
PORT = 3306
USERNAME = "root"
PASSWORD = "3380"
DATABASE = "dbdetect"

app.config[
    'SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{USERNAME}:{PASSWORD}@{HOSTNAME}:{PORT}/{DATABASE}?charset=utf8mb4"

db = SQLAlchemy(app)

# 录像上传函数
@app.route('/recordUpload', methods=['POST'])
@cross_origin(origins='http://localhost:8080')
def record_upload():  # put application's code here
    record = request.files['record']
    # 文件写入磁盘
    record.save('./file/records/' + record.filename)
    # 记录数据库
    with app.app_context():
        with db.engine.connect() as conn:
            # 执行原生SQL语句
            # res = conn.execute(text("insert into file(filename) values (:name)"), [{"name":record.filename}])
            # res = conn.execute(text("insert into file(filename) values ('admin')"))
            res = conn.execute(text("select * from user"))
            for result in res:
                print(result)
            print(res)
    # 建立线程车辆检测
    t=Thread(target=detect_process)
    t.start()
    return result.success()

# 设置
@app.route('/setting/get', methods=['GET'])
@cross_origin(origins='http://localhost:8080')
def get_setting():
    return result.success({
        "SPEED_LIMIT": SPEED_LIMIT,
    })

@app.route('/setting/update', methods=['POST'])
@cross_origin(origins='http://localhost:8080')
def update_setting():
    data = reception.toDict(request.data)
    global SPEED_LIMIT
    SPEED_LIMIT = data['SPEED_LIMIT']
    return result.success()

def detect_process():
    print("======START DETECTION======")
    ve.vehicle_detect()
    print("======END   DETECTION======")
    return True

if __name__ == '__main__':
    app.run()

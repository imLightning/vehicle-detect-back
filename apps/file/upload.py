from flask import request,  json
from utils.sql import insert
from utils.result import Result
import time


# 登录
def upload():
    record = request.files['record']
    sql = 'insert into file(filename) values (%s);'
    timestamp = str(time.time())
    name = timestamp + '_' + record.filename
    insert(sql, name)
    record.save('file/records/' + name)
    return Result.success()

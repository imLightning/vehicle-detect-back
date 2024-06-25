from flask import request,  json
from utils.sql import insert, select, select_all
from utils.result import Result
from models.file import File
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

def get_file():
    sql = 'select * from file;'
    rs = select_all(sql)
    list = []
    for i in rs:
        if i is not None:
            file = File(i[0], i[1], i[2], i[3])

        if file is not None:
            return_dict = Result.to_object(Result.data(file.to_object(file)))
        else:
            return_dict = Result.to_object(Result.data({}))
        list.append(return_dict['data'])
    return_dict = Result.to_object(Result.data(list))
    return json.dumps(return_dict, sort_keys=False)


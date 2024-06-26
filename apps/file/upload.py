import os

from flask import request,  json

from utils import recept
from utils.encoder import DateTimeEncoder
from utils.sql import insert, select, select_all, delete
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
    os.makedirs('file/records/', exist_ok=True)
    record.save('file/records/' + name)
    return Result.success()

def manual_upload():
    f = request.files['file']
    sql = 'insert into file(filename) values (%s);'
    timestamp = str(time.time())
    name = timestamp + '_' + f.filename
    insert(sql, name)
    os.makedirs('file/records/', exist_ok=True)
    f.save('file/records/' + name)
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
    return json.dumps(return_dict, sort_keys=False, cls=DateTimeEncoder)

def insert_res(name, info):
    sql = 'insert into res(filename, info) values (%s, %s);'
    insert(sql, (name, info))
    return 1

def del_file():
    id = recept.to_dict()['id']
    filename = recept.to_dict()['filename']
    path = 'file/records/' + filename
    os.remove(path)
    sql = 'delete from file where id=%s;'
    delete(sql, id)
    return Result.success()

def del_res():
    id = recept.to_dict()['id']
    filename = recept.to_dict()['filename']
    path = 'file/results/' + filename
    os.remove(path)
    sql = 'delete from res where id=%s;'
    delete(sql, id)
    return Result.success()


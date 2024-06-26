import os
from flask import json
from models.violation import Violation
from utils import recept
from utils.encoder import DateTimeEncoder
from utils.sql import insert, select_all, delete
from utils.result import Result

def insert_one(filename):
    sql = 'insert into violation(filename) values (%s);'
    insert(sql, filename)
    return Result.success()

def get_all():
    sql = 'select * from violation;'
    rs = select_all(sql)
    list = []
    for i in rs:
        if i is not None:
            violation = Violation(i[0], i[1], i[2])
        if violation is not None:
            return_dict = Result.to_object(Result.data(violation.to_object(violation)))
        else:
            return_dict = Result.to_object(Result.data({}))
        list.append(return_dict['data'])
    return_dict = Result.to_object(Result.data(list))
    return json.dumps(return_dict, sort_keys=False, cls=DateTimeEncoder)

def del_one():
    id = recept.to_dict()['id']
    filename = recept.to_dict()['filename']
    path = 'file/warning/' + filename
    os.remove(path)
    sql = 'delete from violation where id=%s;'
    delete(sql, id)
    return Result.success()
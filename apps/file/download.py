import json

from flask import send_file, request

from models.res import Res
from utils import recept
from utils.result import Result
from utils.sql import select_all, select
from utils.encoder import DateTimeEncoder


def get_res():
    sql = 'select * from res;'
    rs = select_all(sql)
    list = []
    for i in rs:
        if i is not None:
            res = Res(i[0], i[1], i[2], i[3], i[4])

        if res is not None:
            return_dict = Result.to_object(Result.data(res.to_object(res)))
        else:
            return_dict = Result.to_object(Result.data({}))
        list.append(return_dict['data'])
    return_dict = Result.to_object(Result.data(list))
    return json.dumps(return_dict, sort_keys=False, cls=DateTimeEncoder)

def send_records():
    id = request.args.get('id')
    sql = 'select filename from file where id=%s'
    rs = select(sql, id)
    path = 'file/records/' + rs[0]
    return send_file(path)

def send_res():
    id = request.args.get('id')
    sql = 'select filename from res where id=%s'
    rs = select(sql, id)
    path = 'file/results/' + rs[0]
    return send_file(path, as_attachment=True, conditional=True)

def send_violation():
    id = request.args.get('id')
    sql = 'select filename from violation where id=%s'
    rs = select(sql, id)
    path = 'file/warning/' + rs[0]
    return send_file(path)
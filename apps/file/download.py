import json

from models.res import Res
from utils.result import Result
from utils.sql import select_all
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
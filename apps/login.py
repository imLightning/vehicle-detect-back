from flask import json, request

from utils.sql import select
from utils.result import Result
from models.user import User
from utils.recept import to_dict


# 登录
def to_login():
    user = None
    username = to_dict()['username']
    password = to_dict()['password']

    sql = 'select * from user where username=%s and password=%s;'
    rs = select(sql, (username, password))
    if rs is not None:
        user = User(rs[0], rs[1], rs[2], rs[3])

    if user is not None:
        return_dict = Result.to_object(Result.data(user.to_object(user)))
    else:
        return_dict = Result.to_object(Result.error('账号或密码错误'))
    return json.dumps(return_dict, sort_keys=False)

def is_login(token):
    user = None

    id = token
    print(id)


    sql = 'select * from user where id=%s;'
    rs = select(sql, (id,))
    if rs is not None:
        user = User(rs[0], rs[1], rs[2], rs[3])
    if user is not None:
        return_dict = Result.to_object(Result.data(user.to_object(user)))
    else:
        return_dict = Result.to_object(Result.error('用户不存在'))
    return json.dumps(return_dict, sort_keys=False)

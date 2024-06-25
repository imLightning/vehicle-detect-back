from flask import request,  json

from utils.sql import select
from utils.result import Result
from models.user import User


# 登录
def to_login():
    user = None
    username = ''
    password = ''
    if request.args is not None and 'username' in request.args:
        data = request.args.to_dict()
        username = data.get('username')
        password = data.get('password')
    sql = 'select * from user where username=%s and password=%s;'
    rs = select(sql, (username, password))
    if rs is not None:
        user = User(rs[0], rs[1], rs[2], rs[3])

    if user is not None:
        return_dict = Result.to_object(Result.data(user.to_object(user)))
    else:
        return_dict = Result.to_object(Result.error('账号或密码错误'))
    return json.dumps(return_dict, sort_keys=False)

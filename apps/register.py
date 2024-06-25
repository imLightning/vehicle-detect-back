from flask import request, json

from utils.sql import select, insert
from utils.result import Result

# 注册
def to_register():
    cnt = 0
    msg = ''
    username = ''
    password = ''
    phone = ''
    if request.args is not None and 'username' in request.args:
        data = request.args.to_dict()
        username = data.get('username')
        password = data.get('password')
        phone = data.get('phone')
        sql = 'select * from user where username=%s and password=%s;'
        rs = select(sql, (username, password))
        if rs is not None:
            msg = '用户名已存在'
        else:
            sql = 'insert into user (username, password, phone) values (%s, %s, %s);'
            cnt = insert(sql, (username, password, phone))
            if cnt == 1:
                msg = '注册成功'
            elif cnt == 0:
                msg = '注册失败'

    if len(username) > 0 and len(password) > 0 and len(phone) > 0 and cnt == 1:
        return_dict = Result.to_object(Result.get(200, msg, None))
    else:
        return_dict = Result.to_object(Result.error(msg))
    return json.dumps(return_dict, sort_keys=False)

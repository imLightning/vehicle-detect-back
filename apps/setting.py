from flask import request,  json

from utils import recept
from utils.sql import insert, select, select_all, update
from utils.result import Result
from models.file import File
import time

def get_attr(attr):
    sql = 'select val from setting where attr=%s;'
    rs = select(sql, attr)
    return rs[0]

def update_attr():
    attr = recept.to_dict()['attr']
    val = recept.to_dict()['val']
    sql = 'update setting set val=%s where attr=%s'
    update(sql, (val, attr))
    return Result.success()
from flask import request,  json
from utils.sql import insert, select, select_all
from utils.result import Result
from models.file import File
import time

def get_attr(attr):
    sql = 'select val from setting where attr=%s;'
    rs = select(sql, attr)
    return rs[0]
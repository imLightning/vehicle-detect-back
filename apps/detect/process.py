from apps import setting
from apps.file.state import update_state
from apps.file.upload import insert_res
from utils import recept
from utils.result import Result
from flask import request, json
from threading import Thread
from apps.detect.vehicle import vehicle_detect

def detect_file():
    id = recept.to_dict()['id']
    filename = recept.to_dict()['filename']
    speed_limit = setting.get_attr('SPEED_LIMIT')
    t  = Thread(target=result_process, args=(id, filename, {'speed_limit':speed_limit}))
    t.start()
    return Result.success({})

def result_process(id, filename, attr):
    update_state(id, '检测中')
    info_dict = vehicle_detect(filename, attr)
    # info_dict = {1: 75, 2: 111, 3: 115, 5: 126, 6: 115, 7: 111, 9: 129, 10: 61, 11: 97, 12: 86, 13: 140, 16: 214}
    print(info_dict)
    update_state(id, '已检测')
    new_info_dict = {}
    for key, value in info_dict.items():
        new_key = int(key)
        new_value = int(value)
        new_info_dict[new_key] = new_value
    insert_res(filename, json.dumps(new_info_dict))
    return 1


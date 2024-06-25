import json

def success(data = {}):
    res = {
        "msg": "success",
        "data": data,
    }
    return json.dumps(res)
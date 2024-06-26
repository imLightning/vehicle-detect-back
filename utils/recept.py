import json
from flask import request


def to_dict():
    return json.loads(request.data)
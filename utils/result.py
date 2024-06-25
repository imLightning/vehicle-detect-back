
class Result:
    __code = 0
    __msg = ''
    __data = None

    def __init__(self, code, msg, data):
        if code is not None:
            self.set_code(code)
        if msg is not None:
            self.set_msg(msg)
        if data is not None:
            self.set_data(data)

    def get_code(self):
        return self.__code

    def get_msg(self):
        return self.__msg

    def get_data(self):
        return self.__data

    def set_code(self, code):
        self.__code = code

    def set_msg(self, msg):
        self.__msg = msg

    def set_data(self, data):
        self.__data = data

    @staticmethod
    def ok(msg):
        if msg is None:
            return Result(200, 'ok', None)
        elif msg is not None:
            return Result(200, msg, None)

    @staticmethod
    def code(code):
        return Result(code, str(None), None)

    @staticmethod
    def data(data):
        if data is not None:
            return Result(200, 'ok', data)

    @staticmethod
    def error(msg):
        if msg is None:
            return Result(500, 'error', None)
        elif msg is not None:
            return Result(400, msg, None)

    @staticmethod
    def get(code, msg, data):
        return Result(code, msg, data)

    @staticmethod
    def to_object(self):
        return dict(code=self.get_code(), msg=self.get_msg(), data=self.get_data())

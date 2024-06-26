
class Res:
    __id = 0
    __filename = ''
    __state = ''
    __time = ''
    __info = ''

    def __init__(self, id, filename, state, time, info):
        self.set_id(id)
        self.set_filename(filename)
        self.set_state(state)
        self.set_time(time)
        self.set_info(info)

    def get_id(self):
        return self.__id

    def get_filename(self):
        return self.__filename

    def get_state(self):
        return self.__state

    def get_time(self):
        return self.__time

    def get_info(self):
        return self.__info

    def set_id(self, id):
        self.__id = id

    def set_filename(self, filename):
        self.__filename = filename

    def set_state(self, state):
        self.__state = state

    def set_time(self, time):
        self.__time = time

    def set_info(self, info):
        self.__info = info

    @staticmethod
    def to_object(self):
        return dict(id=self.get_id(), filename=self.get_filename(), state=self.get_state(), time=self.get_time(), info=self.get_info())

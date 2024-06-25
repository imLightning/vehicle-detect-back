
class File:
    __id = 0
    __filename = ''
    __state = ''
    __time = ''

    def __init__(self, id, filename, state, time):
        self.set_id(id)
        self.set_filename(filename)
        self.set_state(state)
        self.set_time(time)

    def get_id(self):
        return self.__id

    def get_filename(self):
        return self.__filename

    def get_state(self):
        return self.__state

    def get_time(self):
        return self.__time

    def set_id(self, id):
        self.__id = id

    def set_filename(self, filename):
        self.__filename = filename

    def set_state(self, state):
        self.__state = state

    def set_time(self, time):
        self.__time = time

    @staticmethod
    def to_object(self):
        return dict(id=self.get_id(), filename=self.get_filename(), state=self.get_state(), time=self.get_time())

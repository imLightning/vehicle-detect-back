
class Violation:
    __id = 0
    __filename = ''
    __time = ''

    def __init__(self, id, filename, time):
        self.set_id(id)
        self.set_filename(filename)
        self.set_time(time)

    def get_id(self):
        return self.__id

    def get_filename(self):
        return self.__filename

    def get_time(self):
        return self.__time

    def set_id(self, id):
        self.__id = id

    def set_filename(self, filename):
        self.__filename = filename

    def set_time(self, time):
        self.__time = time

    @staticmethod
    def to_object(self):
        return dict(id=self.get_id(), filename=self.get_filename(), time=self.get_time())

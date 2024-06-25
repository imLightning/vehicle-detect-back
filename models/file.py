
class User:
    __id = 0
    __filename = ''

    def __init__(self, id, filename):
        self.set_id(id)
        self.set_filename(filename)

    def get_id(self):
        return self.__id

    def get_filename(self):
        return self.__filename

    def set_id(self, id):
        self.__id = id

    def set_filename(self, filename):
        self.__filename = filename

    @staticmethod
    def to_object(self):
        return dict(id=self.get_id(), filename=self.get_filename())

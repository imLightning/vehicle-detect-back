
class User:
    __id = 0
    __username = ''
    __password = ''
    __phone = ''

    def __init__(self, id, username, password, phone):
        self.set_id(id)
        self.set_username(username)
        self.set_password(password)
        self.set_phone(phone)

    def get_id(self):
        return self.__id

    def get_username(self):
        return self.__username

    def get_password(self):
        return self.__password

    def get_phone(self):
        return self.__phone

    def set_id(self, id):
        self.__id = id

    def set_username(self, username):
        self.__username = username

    def set_password(self, password):
        self.__password = password

    def set_phone(self, phone):
        self.__phone = phone

    @staticmethod
    def to_object(self):
        return dict(id=self.get_id(), username=self.get_username(), phone=self.get_phone())

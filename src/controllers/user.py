from src.daos.userDAO import UserDAO
from src.config.config import Config


class UserController:

    def __init__(self, user_id):
        self.__id = user_id
        self.__dao = UserDAO()
        self.__config = Config()

    def new_user(self, user):
        r = self.get_by_id(self.get_id())
        if r.count() <= 0:
            r = self.__dao.new_user(user)
            if r.inserted_id is not None:
                return True
            else:
                return False
        else:
            return False

    def get_by_id(self, user_id):
        users = self.__dao.get_by_id(user_id)
        return users

    def get_id(self):
        return self.__id

    def get_name(self):
        return self.__name

    def set_name(self, name):
        self.__name = name

    def get_users(self):
        return self.__dao.get_users()

    def close_connection(self):
        self.__dao.close_connection()

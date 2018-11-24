from daos.userDAO import UserDAO
from config.config import Config


class UserController:

    def __init__(self, id):
        self._id = id
        self._dao = UserDAO()
        self._config = Config()

    def new_user(self, user):
        r = self.get_by_id(user.get_id())
        if r.count() <= 0:
            r = self._dao.new_user(user)
            if r.inserted_id is not None:
                return True
            else:
                return False
        else:
            return False

    def get_by_id(self, id):
        users = self._dao.get_by_id(id)
        return users

    def enabled_flow(self, flow):
        return self._dao.enabled_flow(self._id, flow)

    def get_id(self):
        return self._id

    def get_name(self):
        return self._name

    def set_name(self, name):
        self._name = name

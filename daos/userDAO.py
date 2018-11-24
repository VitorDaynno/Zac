from pymongo import MongoClient


class UserDAO:

    def __init__(self):
        self._client = MongoClient()
        self._db = self._client.bot_ajudante

    def new_user(self, user):
        users = self._db.users
        users.insert_one({"chat_id": user.get_id(), "name": user.get_name()})

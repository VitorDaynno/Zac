from pymongo import MongoClient
from config.config import Config
from config.logger import logger
import datetime


class UserDAO:

    def __init__(self):
        self._config = Config()
        self._client = MongoClient()
        self._db = self._client[self._config.get_db_name()]

    def new_user(self, user):
        logger.info('[userDAO] Creating a new user')
        collection = self._db.users
        r = collection.insert_one({"chat_id": user.get_id(), "name": user.get_name(), "createdDate": datetime.datetime.now()})
        return r

    def get_by_id(self, id):
        logger.info('[userDAO] Getting user by chat_id: ' + str(id))
        users = self._db.users
        r = users.find({"chat_id": id})
        return r

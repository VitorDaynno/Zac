from pymongo import MongoClient
from config.config import Config
from config.logger import logger
import datetime


class UserDAO:

    def __init__(self):
        self._config = Config()
        self._client = MongoClient(self._config.get_db_server(), 27017)
        self._db = self._client[self._config.get_db_name()]

    def new_user(self, user):
        logger.info('Creating a new user')
        collection = self._db.users
        userEntity = {"chat_id": user.get_id(),
                      "name": user.get_name(),
                      "createdDate": datetime.datetime.now()}
        r = collection.insert_one(userEntity)
        return r

    def get_by_id(self, user_id):
        logger.info('Getting user by chat_id: ' + str(user_id))
        collection = self._db.users
        r = collection.find({"chat_id": user_id})
        return r

    def get_users(self):
        collection = self._db.users
        r = collection.find({})
        return r

    def close_connection(self):
        self._client.close()

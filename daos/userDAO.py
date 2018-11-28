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
        collection = self._db.users
        r = collection.find({"chat_id": id})
        return r

    def enable_flow(self, id, flow):
        logger.info('[userDAO] Enabling flow {0} by chat_id: {1}'.format(flow, id))
        collection = self._db.users
        r = collection.update_one({"chat_id": id}, {"$set": {"inFlow": True, "flow": flow}}, upsert=False)
        return r

    def get_in_flow(self, id):
        logger.info('[userDAO] Getting flow by chat_id: ' + str(id))
        collection = self._db.users
        r = collection.find_one({'chat_id': id})
        return r

    def disable_in_flow(self, id):
        logger.info('[userDAO] Disabling in_flow by chat_id: ' + str(id))
        collection = self._db.users
        r = collection.update_one({"chat_id": id}, {"$set": {"inFlow": False}}, upsert=False)
        return r

    def remove_flow(self, id):
        logger.info('[userDAO] Remove flow by chat_id: ' + str(id))
        collection = self._db.users
        r = collection.update_one({"chat_id": id}, {"$unset": {"flow": 1}}, upsert=False)
        return r

    def update_step(self, step_id, usu_id):
        users = self._db.users
        r = users.update_one({"chat_id": usu_id}, {"$set": {"flow.stage": step_id}}, upsert=False)
        return r
    
    def get_users(self):
        collection = self._db.users
        r = collection.find({})
        return r

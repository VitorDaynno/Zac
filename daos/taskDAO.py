from pymongo import MongoClient
from config.config import Config
from config.logger import logger


class TaskDAO:

    def __init__(self):
        self._config = Config()
        self._client = MongoClient(self._config.get_db_server(), 27017)
        self._db = self._client[self._config.get_db_name()]

    def new_task(self, name, usu_id):
        tasks = self._db.tasks
        r = tasks.insert_one({"name": name, "usuId": usu_id, "inProcess": True})
        return r

    def update_date(self, date, usu_id):
        tasks = self._db.tasks
        r = tasks.update_one({"usuId": usu_id, "inProcess": True}, {"$set": {"date": date}}, upsert=False)
        return r

    def disable_in_process(self, usu_id):
        collection = self._db.tasks
        r = collection.update_one({"usuId": usu_id, "inProcess": True}, {"$set": {"inProcess": False}}, upsert=False)
        return r

    def get_tasks(self, filter):
        tasks = self._db.tasks
        tasks = tasks.find(filter)
        return tasks

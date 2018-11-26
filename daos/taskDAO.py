from pymongo import MongoClient
from config.config import Config
from config.logger import logger


class TaskDAO:

    def __init__(self):
        self._config = Config()
        self._client = MongoClient()
        self._db = self._client[self._config.get_db_name()]

    def new_task(self, name, usu_id):
        tasks = self._db.tasks
        r = tasks.insert_one({"name": name, "usuId": usu_id, "inProcess": True})
        return r

    def get_tasks(self, id):
        tasks = self._db.tasks
        tasks = tasks.find({"usuId": id})
        return tasks

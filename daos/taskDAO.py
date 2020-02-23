from pymongo import MongoClient
from bson.objectid import ObjectId

from config.config import Config
from config.logger import logger


class TaskDAO:

    def __init__(self):
        self._config = Config()
        self._client = MongoClient(self._config.get_db_server(), 27017)
        self._db = self._client[self._config.get_db_name()]

    def save_task(self, task):
        tasks = self._db.tasks
        r = tasks.insert_one(task)
        return r

    def get_tasks(self, search_filter):
        tasks = self._db.tasks
        tasks = tasks.find(search_filter)
        return tasks

    def close_connection(self):
        self._client.close()

    def conclude_task(self, task_id):
        logger.info("Conclude task {0}".format(task_id))
        tasks = self._db.tasks
        tasks.update_one(
            {"_id": ObjectId(task_id)},
            {"$set": {"isConclude": True}}
        )

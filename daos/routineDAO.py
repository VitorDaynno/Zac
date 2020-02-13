from pymongo import MongoClient

from config.config import Config
from config.logger import logger


class RoutineDAO:

    def __init__(self):
        logger.info("Started routineDAO")
        self._config = Config()
        self._client = MongoClient(self._config.get_db_server(), 27017)
        self._db = self._client[self._config.get_db_name()]

    def save_routine(self, routine):
        logger.info("Started save routine")
        routines = self._db.routines
        r = routines.insert_one(routines)
        return r

    def close_connection(self):
        logger.info("Closing connection")
        self._client.close()

from pymongo import MongoClient
from bson.objectid import ObjectId

from src.config.config import Config
from src.config.logger import logger


class RoutineDAO:

    def __init__(self):
        logger.info("Started routineDAO")
        self.__config = Config()
        self.__client = MongoClient(self.__config.get_db_server(), 27017)
        self.__db = self.__client[self.__config.get_db_name()]

    def save_routine(self, routine):
        logger.info("Started save routine")
        routines = self.__db.routines
        r = routines.insert_one(routine)
        return r

    def get_routines(self, search_filter):
        routine = self.__db.routines
        routines = routine.find(search_filter)
        return routines

    def close_connection(self):
        logger.info("Closing connection")
        self.__client.close()

    def update_last_created_date(self, routine_id, date):
        logger.info("Updating date in routine {0}".format(routine_id))
        routine = self.__db.routines
        routine.update_one(
            {"_id": ObjectId(routine_id)},
            {"$set": {"lastCreatedDate": date}}
        )

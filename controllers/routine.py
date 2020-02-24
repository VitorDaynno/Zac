from daos.routineDAO import RoutineDAO
from config.logger import logger
from helpers.dateHelper import DateHelper
from helpers.redisHelper import RedisHelper

import json


class RoutineController:

    def __init__(self, usu_id):
        logger.info("Initialize RoutineController")
        self.__usu_id = usu_id
        self.__dao = RoutineDAO()
        self.__helper = DateHelper()
        self.__redis = RedisHelper()

    def set_name(self, name):
        try:
            logger.info("Setting name {0}".format(name))

            index = "createRoutine§{0}".format(self.__usu_id)
            value = json.dumps({"name": name})

            self.__redis.set_value(index, value)
        except Exception as error:
            logger.error("An error occurred: {0}".format(error))
            raise error

    def set_hour(self, hour):
        try:
            logger.info("Setting hour {0}".format(hour))

            index = "createRoutine§{0}".format(self.__usu_id)

            is_valid = self.__helper.is_valid_time(hour)

            if not is_valid:
                raise Exception("Time is invalid")

            routine = self.__redis.get_value(index)
            routine = json.loads(routine)
            routine["hour"] = hour
            value = json.dumps(routine)

            self.__redis.set_value(index, value)
        except Exception as error:
            logger.error("An error occurred: {0}".format(error))
            raise error

    def set_days(self, days):
        try:
            logger.info("Setting days {0}".format(days))

            index = "createRoutine§{0}".format(self.__usu_id)
            routine = self.__redis.get_value(index)
            routine = json.loads(routine)
            routine["days"] = days
            value = json.dumps(routine)

            self.__redis.set_value(index, value)
        except Exception as error:
            logger.error("An error occurred: {0}".format(error))
            raise error

    def save_routine(self, routine):
        try:
            logger.info("Saving routine '{0}'".format(routine))

            index = "createRoutine§{0}".format(self.__usu_id)
            self.routine = self.__redis.get_value(index)
            self.routine = json.loads(self.routine)

            self.routine["userId"] = self.__usu_id
            self.routine["isActive"] = True
            self.routine["isEnabled"] = True

            self.__dao.save_routine(self.routine)

            self.close_connection()
            self.__redis.delete_key(index)
        except Exception as error:
            logger.error("An error occurred: {0}".format(error))

    def get_routines(self, search_filter):
        logger.info("Getting routines by database")
        routines = self.__dao.get_routines(search_filter)
        return list(routines)

    def close_connection(self):
        logger.info("Closing connection to database")
        self.__dao.close_connection()

    def update_last_created_date(self, routine_id, date):
        logger.info("Updating date in routine {0}".format(routine_id))
        self.__dao.update_last_created_date(routine_id, date)

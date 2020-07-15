from src.daos.routineDAO import RoutineDAO
from src.config.logger import logger
from src.helpers.dateHelper import DateHelper

import json


class RoutineController:

    def __init__(self, user_id, redis_helper):
        logger.info("Initialize RoutineController")
        self._user_id = user_id
        self._dao = RoutineDAO()
        self._helper = DateHelper()
        self._redis = redis_helper

    def set_name(self, name):
        try:
            logger.info("Setting name {0}".format(name))

            if name is None:
                raise Exception("Name is required")

            if name == "":
                raise Exception("Name should not be empty")

            index = "createRoutine§{0}".format(self._user_id)
            value = json.dumps({"name": name})

            self._redis.set_value(index, value)
            return "{} set successfully".format(name)
        except Exception as error:
            logger.error("An error occurred: {0}".format(error))
            raise error

    def set_hour(self, hour):
        try:
            logger.info("Setting hour {0}".format(hour))

            index = "createRoutine§{0}".format(self._user_id)

            is_valid = self._helper.is_valid_time(hour)

            if not is_valid:
                raise Exception("Time is invalid")

            routine = self._redis.get_value(index)
            routine = json.loads(routine)
            routine["hour"] = hour
            value = json.dumps(routine)

            self._redis.set_value(index, value)
        except Exception as error:
            logger.error("An error occurred: {0}".format(error))
            raise error

    def set_days(self, days):
        try:
            logger.info("Setting days {0}".format(days))

            index = "createRoutine§{0}".format(self._user_id)
            routine = self._redis.get_value(index)
            routine = json.loads(routine)
            routine["days"] = days
            value = json.dumps(routine)

            self._redis.set_value(index, value)
        except Exception as error:
            logger.error("An error occurred: {0}".format(error))
            raise error

    def save_routine(self, routine):
        try:
            logger.info("Saving routine '{0}'".format(routine))

            index = "createRoutine§{0}".format(self._user_id)
            self.routine = self._redis.get_value(index)
            self.routine = json.loads(self.routine)

            self.routine["userId"] = self._user_id
            self.routine["isActive"] = True
            self.routine["isEnabled"] = True

            self._dao.save_routine(self.routine)

            self.close_connection()
            self._redis.delete_key(index)
        except Exception as error:
            logger.error("An error occurred: {0}".format(error))

    def get_routines(self, search_filter):
        logger.info("Getting routines by database")
        routines = self._dao.get_routines(search_filter)
        return list(routines)

    def close_connection(self):
        logger.info("Closing connection to database")
        self._dao.close_connection()

    def update_last_created_date(self, routine_id, date):
        logger.info("Updating date in routine {0}".format(routine_id))
        self._dao.update_last_created_date(routine_id, date)

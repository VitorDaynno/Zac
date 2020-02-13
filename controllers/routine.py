from daos.routineDAO import RoutineDAO
from config.logger import logger
from helpers.dateHelper import DateHelper


class RoutineController:

    def __init__(self, usu_id):
        logger.info("Initialize RoutineController")
        self.__usu_id = usu_id
        self.__dao = RoutineDAO()
        self.__helper = DateHelper()

    def save_routine(self, routine):
        try:
            logger.info("Saving routine '{0}'".format(routine))
            self.routine = {}
            self.routine["name"] = routine["name"]

            days = routine["days"]
            hour = routine["hour"]

            self.routine["days"] = days
            self.routine["hour"] = hour
            self.routine["userId"] = self.__usu_id
            self.routine["isActive"] = True
            self.routine["isEnabled"] = True

            self.__dao.save_routine(self.routine)
            self.close_connection()
        except Exception as error:
            logger.error("An error occurred: {0}".format(error))

    def close_connection(self):
        logger.info("Closing connection to databases")
        self.__dao.close_connection()

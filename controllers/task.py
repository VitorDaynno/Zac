from datetime import datetime
import json

from daos.taskDAO import TaskDAO
from config.logger import logger
from helpers.dateHelper import DateHelper


class TaskController:

    def __init__(self, user_id, redis_helper):
        logger.info("Initialize TaskController")
        self.__user_id = user_id
        self.__dao = TaskDAO()
        self.__helper = DateHelper()
        self.__redis = redis_helper

    def save_task(self, task):
        logger.info("Saving task '" + str(task) + "'")
        self.task = {}
        self.task["name"] = task["name"]

        date = task["date"].split('/')
        hour = task["hour"].split(":")
        new_date = datetime(int(date[2]), int(date[1]), int(date[0]),
                            int(hour[0]), int(hour[1]), 0)

        self.task["date"] = self.__helper.to_UTC(new_date)
        self.task["usuId"] = self.__usu_id
        self.task["isConclude"] = False

        self.__dao.save_task(self.task)
        self.close_connection()

    def get_usu_id(self):
        logger.info("Getting usu_id")
        return self.__usu_id

    def get_tasks(self, search_filter):
        logger.info("Getting tasks by usu_id: " + str(self.__usu_id))
        filters = {'usuId': self.__usu_id}
        if 'date' in search_filter:
            filters["date"] = search_filter["date"]
        if "isConclude" in search_filter:
            filters["isConclude"] = search_filter["isConclude"]
        return list(self.__dao.get_tasks(filters))

    def close_connection(self):
        logger.info("Closing connection to databases")
        self.__dao.close_connection()

    def conclude_task(self, task_id):
        logger.info("Conclude task {0}".format(task_id))
        self.__dao.conclude_task(task_id)

    def set_name(self, name):
        try:
            logger.info("Setting name {0}".format(name))

            index = "createTask§{0}".format(self.__user_id)
            value = json.dumps({"name": name})

            self.__redis.set_value(index, value)
        except Exception as error:
            logger.error("An error occurred: {0}".format(error))
            raise error

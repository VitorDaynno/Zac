from datetime import datetime
from pytz import timezone
import pytz

from daos.taskDAO import TaskDAO
from config.logger import logger


class TaskController:

    def __init__(self, usu_id):
        logger.info("Initialize TaskController")
        self.__usu_id = usu_id
        self.__dao = TaskDAO()

    def save_task(self, task):
        logger.info("Saving task '" + str(task) + "'")
        self.task = {}
        self.task["name"] = task["name"]

        date = task["date"].split('/')
        hour = task["hour"].split(":")
        new_date = datetime(int(date[2]), int(date[1]), int(date[0]),
                            int(hour[0]), int(hour[1]), 0)

        self.task["date"] = self.__to_UTC(new_date)
        self.task["usuId"] = self.__usu_id
        self.task["isConclude"] = False

        self.__dao.save_task(self.task)
        self.close_connection()

    def get_usu_id(self):
        logger.info("Getting usu_id")
        return self.__usu_id

    def get_tasks(self, filter):
        logger.info("Getting tasks by usu_id: " + str(self.__usu_id))
        filters = {'usuId': self.__usu_id}
        if 'date' in filter:
            filters["date"] = filter["date"]
        if "isConclude" in filter:
            filters["isConclude"] = filter["isConclude"]
        return list(self.__dao.get_tasks(filters))

    def __to_UTC(self, date):
        tz = timezone('America/Sao_Paulo')
        return tz.normalize(tz.localize(date)).astimezone(pytz.utc)

    def close_connection(self):
        logger.info("Closing connection to databases")
        self.__dao.close_connection()

    def conclude_task(self, task_id):
        logger.info("Conclude task {0}".format(task_id))
        self.__dao.conclude_task(task_id)

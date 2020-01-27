from datetime import datetime, timedelta
from pytz import timezone
import pytz

from daos.taskDAO import TaskDAO
from config.logger import logger


class TaskController:

    def __init__(self, usu_id):
        logger.info("Initialize TaskController")
        self._usu_id = usu_id
        self._dao = TaskDAO()

    def save_task(self, task):
        logger.info("Saving task '" + str(task) + "'")
        self.task = {}
        self.task["name"] = task["name"]

        date = task["date"].split('/')
        hour = task["hour"].split(":")
        new_date = datetime(int(date[2]), int(date[1]), int(date[0]),
                            int(hour[0]), int(hour[1]), 0)

        self.task["date"] = self._to_UTC(new_date)
        self.task["usuId"] = self._usu_id

        self._dao.save_task(self.task)
        self.close_connection()

    def get_usu_id(self):
        logger.info("Getting usu_id")
        return self._usu_id

    def get_tasks(self, filter):
        logger.info("Getting tasks by usu_id: " + str(self._usu_id))
        filters = {'usuId': self._usu_id}
        if 'date' in filter:
            filters["date"] = filter["date"]
        if "isConclude" in filter:
            filters["isConclude"] = filter["isConclude"]
        return list(self._dao.get_tasks(filters))

    def _to_UTC(self, date):
        tz = timezone('America/Sao_Paulo')
        return tz.normalize(tz.localize(date)).astimezone(pytz.utc)

    def close_connection(self):
        logger.info("Closing connection to databases")
        self._dao.close_connection()

from datetime import datetime
import json

from daos.taskDAO import TaskDAO
from config.logger import logger
from helpers.dateHelper import DateHelper


class TaskController:

    def __init__(self, user_id, redis_helper):
        logger.info("Initialize TaskController")
        self._user_id = user_id
        self._dao = TaskDAO()
        self._helper = DateHelper()
        self._redis = redis_helper

    def save_task(self, task):
        logger.info("Saving task")

        task["userId"] = self._user_id
        task["isConclude"] = False

        self._dao.save_task(task)
        self.close_connection()

    def create_task(self, time):
        logger.info("Creating task")
        self.task = {}

        index = "createTask§{0}".format(self._user_id)

        is_valid = self._helper.is_valid_time(time)

        if not is_valid:
            raise ValueError("Time is invalid")

        task = self._redis.get_value(index)
        task = json.loads(task)

        name = task["name"]
        date = task["date"]

        new_date = self._helper.concat_to_datetime(date, time)

        self.task["name"] = name
        self.task["date"] = self._helper.to_UTC(new_date)

        self.save_task(self.task)

    def get_user_id(self):
        logger.info("Getting user_id")
        return self._user_id

    def get_tasks(self, search_filter):
        logger.info("Getting tasks by user_id: " + str(self._user_id))
        filters = {'userId': self._user_id}
        if 'date' in search_filter:
            filters["date"] = search_filter["date"]
        if "isConclude" in search_filter:
            filters["isConclude"] = search_filter["isConclude"]
        return list(self._dao.get_tasks(filters))

    def close_connection(self):
        logger.info("Closing connection to databases")
        self._dao.close_connection()

    def conclude_task(self, task_id):
        logger.info("Conclude task {0}".format(task_id))
        self._dao.conclude_task(task_id)

    def set_name(self, name):
        try:
            logger.info("Setting name {0}".format(name))

            index = "createTask§{0}".format(self._user_id)
            value = json.dumps({"name": name})

            self._redis.set_value(index, value)
        except Exception as error:
            logger.error("An error occurred: {0}".format(error))
            raise error
    
    def set_date(self, date):
        try:
            logger.info("Setting date {0}".format(date))

            index = "createTask§{0}".format(self._user_id)

            is_valid = self._helper.is_valid_date(date)

            if not is_valid:
                raise ValueError("Date is invalid")

            task = self._redis.get_value(index)
            task = json.loads(task)
            task["date"] = date
            value = json.dumps(task)

            self._redis.set_value(index, value)
        except Exception as error:
            logger.error("An error occurred: {0}".format(error))
            raise error
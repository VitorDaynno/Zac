from daos.taskDAO import TaskDAO
from config.config import Config
import datetime


class TaskController:

    def __init__(self, name, day, hour, usu_id):
        self._name = name
        self._day = day
        self._hour = hour
        self._usu_id = usu_id
        self._dao = TaskDAO()
        self._config = Config()

    def new_task(self, task):
        return self._dao.new_task(task)

    def get_name(self):
        return self._name

    def get_date(self):
        x = datetime.datetime(2002, 10, 27, 6, 0, 0)
        return x

    def get_usu_id(self):
        return self._usu_id

    def get_tasks(self):
        return self._dao.get_tasks(self._usu_id)

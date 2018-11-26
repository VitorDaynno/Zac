from daos.taskDAO import TaskDAO
from config.config import Config
import datetime


class TaskController:

    def __init__(self, usu_id):
        self._usu_id = usu_id
        self._dao = TaskDAO()
        self._config = Config()

    def new_task(self, step, text):
        if step == 'name':
            return self._dao.new_task(text, self._usu_id)
        if step == 'date':
            return self._dao.update_date(text, self._usu_id)

    def get_usu_id(self):
        return self._usu_id

    def get_tasks(self):
        return self._dao.get_tasks(self._usu_id)

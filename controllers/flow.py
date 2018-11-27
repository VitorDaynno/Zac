from daos.flowDAO import FlowDAO
from controllers.task import TaskController
from controllers.user import UserController
from config.logger import logger


class FlowController:

    def __init__(self, flow, message, usu_id):
        self._type = flow['type']
        self._status = flow['stage']
        self._message = message
        self._usu_id = usu_id
        self._dao = FlowDAO()

    def execute_step(self):
        logger.info(('[FlowController] Execute a step {0} by flow: '.format(self._status)) + self._type)
        if self._type == 'newTask' and self._status == 0:
            task = TaskController(self._usu_id)
            task.new_task('name', self._message.text)
        elif self._type == 'newTask' and self._status == 1:
            task = TaskController(self._usu_id)
            r = task.new_task('date', self._message.text)
            task.remove_in_process(r)

    def get_next_step(self):
        logger.info('[FlowController] Getting a next step by flow: ' + self._type)
        return self._dao.get_next_step(self._type, self._status)

    def update_step(self, step_id):
        logger.info('[FlowController] Updating a step by flow: ' + self._type)
        user = UserController(self._usu_id)
        user.update_step(step_id)

import unittest

from src.controllers.routine import RoutineController
from src.helpers.redisHelper import RedisHelper


class RoutineControllerTest(unittest.TestCase):

    def test_set_name_without_name(self):
        try:
            redis_helper = RedisHelper()
            routineController = RoutineController(None, redis_helper)
            routineController.set_name(None)
            self.fail()
        except Exception as error:
            self.assertEqual(error.args[0], "Name is required")

    def test_set_name_with_empty_name(self):
        try:
            redis_helper = RedisHelper()
            routineController = RoutineController(None, redis_helper)
            routineController.set_name("")
            self.fail()
        except Exception as error:
            self.assertEqual(error.args[0], "Name should not be empty")

    def test_set_name_with_name(self):
        redis_helper = RedisHelper()
        routineController = RoutineController(None, redis_helper)
        routineController.set_name("Test")
        self.fail()

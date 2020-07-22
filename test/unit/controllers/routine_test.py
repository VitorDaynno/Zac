import unittest

from unittest.mock import MagicMock

from src.controllers.routine import RoutineController
from src.helpers.redisHelper import RedisHelper


class RoutineControllerTest(unittest.TestCase):

    def test_set_name_without_name(self):
        try:
            redis_helper = RedisHelper()
            routineController = RoutineController(None, redis_helper)
            set_value_mock = MagicMock()
            redis_helper.set_value = set_value_mock
            routineController.set_name(None)
            self.fail()
        except Exception as error:
            self.assertEqual(error.args[0], "Name is required")
            set_value_mock.assert_not_called()

    def test_set_name_with_empty_name(self):
        try:
            redis_helper = RedisHelper()
            routineController = RoutineController(None, redis_helper)
            set_value_mock = MagicMock()
            redis_helper.set_value = set_value_mock
            routineController.set_name("")
            self.fail()
        except Exception as error:
            self.assertEqual(error.args[0], "Name should not be empty")
            set_value_mock.assert_not_called()

    def test_set_name_with_name_but_failed(self):
        redis_helper = RedisHelper()
        routineController = RoutineController(1, redis_helper)

        set_value_mock = MagicMock(side_effect=Exception('Error'))
        redis_helper.set_value = set_value_mock

        try:
            routineController.set_name("Test")
            self.fail()
        except Exception as error:
            self.assertEqual(error.args[0], "Error")
            set_value_mock.assert_called_with(
                "createRoutine§1", '{"name": "Test"}')

    def test_set_name_with_name(self):
        redis_helper = RedisHelper()
        routineController = RoutineController(1, redis_helper)

        set_value_mock = MagicMock(return_value=True)
        redis_helper.set_value = set_value_mock

        r = routineController.set_name("Test")

        self.assertEqual(r, "Test set successfully")
        set_value_mock.assert_called_once()
        set_value_mock.assert_called_with(
            "createRoutine§1", '{"name": "Test"}')

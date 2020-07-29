import unittest

from unittest.mock import MagicMock

from src.controllers.routine import RoutineController
from src.helpers.redisHelper import RedisHelper
from src.helpers.dateHelper import DateHelper


class SetNameTest(unittest.TestCase):

    def setUp(self):
        self.redis_helper = RedisHelper()
        self.date_helper = DateHelper()
        self.set_value_mock = MagicMock()
        self.redis_helper.set_value = self.set_value_mock

        self.routineController = RoutineController(
            1,
            self.redis_helper,
            self.date_helper
        )

    def test_set_name_without_name(self):
        try:
            self.routineController.set_name(None)
            self.fail()
        except Exception as error:
            self.assertEqual(error.args[0], "Name is required")
            self.set_value_mock.assert_not_called()

    def test_set_name_with_empty_name(self):
        try:
            self.routineController.set_name("")
            self.fail()
        except Exception as error:
            self.assertEqual(error.args[0], "Name should not be empty")
            self.set_value_mock.assert_not_called()

    def test_set_name_with_name_but_failed(self):
        try:
            self.set_value_mock.side_effect = Exception('Error')

            self.routineController.set_name("Test")

            self.fail()
        except Exception as error:
            self.assertEqual(error.args[0], "Error")
            self.set_value_mock.assert_called_with(
                "createRoutine§1", '{"name": "Test"}')

    def test_set_name_with_name(self):
        self.set_value_mock.return_value = True

        r = self.routineController.set_name("Test")

        self.assertEqual(r, "Test set successfully")
        self.set_value_mock.assert_called_once()
        self.set_value_mock.assert_called_with(
            "createRoutine§1", '{"name": "Test"}')

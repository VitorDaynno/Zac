import unittest

from unittest.mock import MagicMock

from src.controllers.routine import RoutineController
from src.helpers.redisHelper import RedisHelper
from src.helpers.dateHelper import DateHelper


class SetHourTest(unittest.TestCase):

    def setUp(self):
        self.redis_helper = RedisHelper()
        self.date_helper = DateHelper()

        self.is_valid_time_mock = MagicMock()
        self.set_value_mock = MagicMock()
        self.get_value_mock = MagicMock()

        self.date_helper.is_valid_time = self.is_valid_time_mock
        self.redis_helper.set_value = self.set_value_mock
        self.redis_helper.get_value = self.get_value_mock

        self.routineController = RoutineController(
            2,
            self.redis_helper,
            self.date_helper
        )

    def test_set_hour_without_hour(self):
        try:
            self.is_valid_time_mock.return_value = False

            self.routineController.set_hour(None)
            self.fail()
        except Exception as error:
            self.assertEqual(error.args[0], "Time is invalid")
            self.is_valid_time_mock.assert_called_once()
            self.is_valid_time_mock.assert_called_with(None)
            self.get_value_mock.assert_not_called()
            self.set_value_mock.assert_not_called()

    def test_set_hour_with_empty_string(self):
        try:
            self.is_valid_time_mock.return_value = False

            self.routineController.set_hour("")
            self.fail()
        except Exception as error:
            self.assertEqual(error.args[0], "Time is invalid")
            self.is_valid_time_mock.assert_called_once()
            self.is_valid_time_mock.assert_called_with("")
            self.get_value_mock.assert_not_called()
            self.set_value_mock.assert_not_called()

    def test_set_hour_but_get_redis_failed(self):
        try:
            self.is_valid_time_mock.return_value = True
            self.get_value_mock.side_effect = Exception('Error')

            self.routineController.set_hour("00:04")
            self.fail()
        except Exception as error:
            self.assertEqual(error.args[0], "Error")
            self.is_valid_time_mock.assert_called_once()
            self.get_value_mock.assert_called_once()
            self.get_value_mock.assert_called_with("createRoutine§2")
            self.set_value_mock.assert_not_called()

    def test_set_hour_but_set_redis_failed(self):
        try:
            self.is_valid_time_mock.return_value = True
            self.get_value_mock.return_value = '{"name": "test"}'
            self.set_value_mock.side_effect = Exception('Error')

            self.routineController.set_hour("00:04")
            self.fail()
        except Exception as error:
            self.assertEqual(error.args[0], "Error")
            self.is_valid_time_mock.assert_called_once()
            self.get_value_mock.assert_called_once()
            self.get_value_mock.assert_called_with("createRoutine§2")
            self.set_value_mock.assert_called_once()
            self.set_value_mock.assert_called_with(
                "createRoutine§2",
                '{"name": "test", "hour": "00:04"}'
            )

    def test_set_hour_with_hour(self):
        self.is_valid_time_mock.return_value = True
        self.get_value_mock.return_value = '{"name": "test"}'
        self.set_value_mock.return_value = True

        r = self.routineController.set_hour("22:43")

        self.assertEqual(r, "22:43 set successfully")
        self.is_valid_time_mock.assert_called_once()
        self.get_value_mock.assert_called_once()
        self.get_value_mock.assert_called_with("createRoutine§2")
        self.set_value_mock.assert_called_once()
        self.set_value_mock.assert_called_with(
            "createRoutine§2",
            '{"name": "test", "hour": "22:43"}'
        )

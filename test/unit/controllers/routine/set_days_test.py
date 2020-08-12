import unittest

from unittest.mock import MagicMock

from src.controllers.routine import RoutineController
from src.helpers.redisHelper import RedisHelper


class SetHourTest(unittest.TestCase):

    def setUp(self):
        self.redis_helper = RedisHelper()

        self.get_value_mock = MagicMock()
        self.set_value_mock = MagicMock()

        self.redis_helper.get_value = self.get_value_mock
        self.redis_helper.set_value = self.set_value_mock

        self.routineController = RoutineController(
            3,
            self.redis_helper,
            None
        )

    def test_set_days_but_get_redis_failed(self):
        try:
            self.get_value_mock.side_effect = Exception('Error')

            self.routineController.set_days([0, 3])
            self.fail()
        except Exception as error:
            self.assertEqual(error.args[0], "Error")
            self.get_value_mock.assert_called_once()
            self.get_value_mock.assert_called_with("createRoutine§3")
            self.set_value_mock.assert_not_called()

    def test_set_days_but_set_redis_failed(self):
        try:

            self.get_value_mock.return_value = '{"name": "test"}'
            self.set_value_mock.side_effect = Exception('Error')

            self.routineController.set_days([0, 2])
            self.fail()
        except Exception as error:
            self.assertEqual(error.args[0], "Error")
            self.get_value_mock.assert_called_once()
            self.get_value_mock.assert_called_with("createRoutine§3")
            self.set_value_mock.assert_called_once()
            self.set_value_mock.assert_called_with(
                "createRoutine§3",
                '{"name": "test", "days": [0, 2]}'
            )

    def test_set_days_with_days(self):
        self.get_value_mock.return_value = '{"name": "test"}'
        self.set_value_mock.return_value = True

        r = self.routineController.set_days([2, 5])

        self.assertEqual(r, "days set successfully")
        self.get_value_mock.assert_called_once()
        self.get_value_mock.assert_called_with("createRoutine§3")
        self.set_value_mock.assert_called_once()
        self.set_value_mock.assert_called_with(
            "createRoutine§3",
            '{"name": "test", "days": [2, 5]}'
        )

import unittest
from unittest.mock import patch, MagicMock
import data_procession
from datetime import datetime

class TestCalculateOnlineTime(unittest.TestCase):
    def setUp(self):
        self.user = {'userId': '1', 'isOnline': True, 'onlinePeriods': [['2023-10-09T14:14:17', '2023-10-09T15:14:17']]}

    def test_calculate_online_time_should_return_total_seconds_online(self):
        result = data_procession.calculate_online_time(self.user)
        self.assertEqual(result, 3600)

    def test_calculate_days_should_return_one_when_called_with_same_day(self):
        result = data_procession.calculate_days(self.user)
        self.assertEqual(result, 1)

    def test_calculate_days_should_return_two_when_called_with_different_days(self):
        self.user['onlinePeriods'] = [['2023-10-09T14:14:17', '2023-10-10T15:14:17']]
        result = data_procession.calculate_days(self.user)
        self.assertEqual(result, 2)

if __name__ == '__main__':
    unittest.main()
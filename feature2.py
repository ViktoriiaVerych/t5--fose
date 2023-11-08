import unittest
from unittest.mock import patch, MagicMock
import data_procession
from datetime import datetime


class TestCalculateDays(unittest.TestCase):
    def setUp(self):
        super().setUp()
        self.user = TestDataFactory.create_user_data()

    def test_calculate_days_should_return_total_days(self):
        result = data_procession.calculate_days(self.user)
        self.assertEqual(result, 2)

    def test_calculate_days_should_return_one_day_when_called_with_same_day_and_none_end(self):
        self.update_user_data()
        result = data_procession.calculate_days(self.user)
        self.assertEqual(result, 1)


class TestCalculateAverageTimes(unittest.TestCase):
    def setUp(self):
        super().setUp()
        self.user = TestDataFactory.create_user_data()

    def test_calculate_average_times_should_return_weekly_and_daily_average(self):
        weekly_average, daily_average = data_procession.calculate_average_times(self.user)
        self.assertAlmostEqual(weekly_average, 315000.0, delta=0.001)
        self.assertAlmostEqual(daily_average, 45000.0, delta=0.001)

    def test_calculate_average_times_should_return_zero_when_called_with_no_online_periods(self):
        self.user = TestDataFactory.create_user_data(isOnline=False, onlinePeriods=[])
        weekly_average, daily_average = data_procession.calculate_average_times(self.user)
        self.assertAlmostEqual(weekly_average, 0.0, delta=0.001)
        self.assertAlmostEqual(daily_average, 0.0, delta=0.001)

    def test_calculate_average_times_should_return_correct_values_when_called_with_multiple_online_periods(self):
        test_cases = [
            {
                'online_periods': [['2023-10-09T14:14:17', '2023-10-09T15:14:17']],
                'expected_weekly_average': 25200.0,
                'expected_daily_average': 3600.0
            },
            {
                'online_periods': [['2023-10-10T14:14:17', '2023-10-10T15:14:17']],
                'expected_weekly_average': 25200.0,
                'expected_daily_average': 3600.0
            }
        ]

        for test_case in test_cases:
            with self.subTest(test_case=test_case):
                self.user = {'userId': '1', 'isOnline': True, 'onlinePeriods': test_case['online_periods']}
                weekly_average, daily_average = data_procession.calculate_average_times(self.user)
                self.assertAlmostEqual(weekly_average, test_case['expected_weekly_average'], delta=0.001)
                self.assertAlmostEqual(daily_average, test_case['expected_daily_average'], delta=0.001)


if __name__ == "__main__":
    unittest.main()
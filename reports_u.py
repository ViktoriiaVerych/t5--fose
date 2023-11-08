import logging
import unittest
from datetime import datetime, timedelta
import json
from unittest.mock import patch, mock_open

now = datetime.now().isoformat()
TEN_SECONDS = 10
TWENTY_SECONDS = 20
THIRTY_SECONDS = 30

class User:
    def __init__(self, user_id, is_online, last_seen_date, online_periods):
        self.user_id = user_id
        self.is_online = is_online
        self.last_seen_date = last_seen_date
        self.online_periods = online_periods

user = User('test_user', True, now, [
    [now, (datetime.now() + timedelta(seconds=TEN_SECONDS)).isoformat()],
    [(datetime.now() + timedelta(seconds=TWENTY_SECONDS)).isoformat(), (datetime.now() + timedelta(seconds=THIRTY_SECONDS)).isoformat()]
])

def calculate_average_times(user):
    # Calculate average times
    daily_average = 0
    weekly_average = 0
    # Calculation logic here
    return weekly_average, daily_average

def calculate_min_max(user):
    # Calculate min and max times
    min_time = 0
    max_time = 0
    # Calculation logic here
    return min_time, max_time

@patch('builtins.open', new_callable=mock_open)
@patch('json.load')
@patch('json.dump')
def test_generate_report(mock_dump, mock_load, mock_open):
    mock_load.return_value = [{"userId": "test_user", "onlinePeriods": [["2023-01-01T00:00:00", "2023-01-01T00:10:00"]]}]
    generate_report('test_report', ['dailyAverage', 'total', 'weeklyAverage'], ['test_user'])
    args, _ = mock_dump.call_args
    report_data = args[0]
    assert report_data == {'test_user': {'dailyAverage': 20, 'weeklyAverage': 140, 'total': 1}}

def generate_report(report_name, report_fields, user_ids):
    # Generate report
    report_data = {}
    # Report generation logic here
    return report_data

if __name__ == "__main__":
    logging.basicConfig(filename='app.log', level=logging.DEBUG)
    logging.debug('Calculating average times')
    weekly_average, daily_average = calculate_average_times(user)
    logging.debug(f'Daily average: {daily_average}')
    logging.debug(f'Weekly average: {weekly_average}')

    logging.debug('Calculating min and max times')
    min_time, max_time = calculate_min_max(user)
    logging.debug(f'Min time: {min_time}')
    logging.debug(f'Max time: {max_time}')

    test_generate_report()
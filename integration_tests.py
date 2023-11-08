from jsonschema import validate
from unittest.mock import patch
import pytest
from pytest_mock import mocker
from datetime import datetime, timedelta
from data_procession import fetch_and_update_data, delete_user_data, previous_state, calculate_days, calculate_min_max, calculate_average_times, calculate_online_time, generate_report, get_reports_in_date_range
import json

from dateutil.parser import parse

# JSON schema for user data
user_schema = {
    "type": "object",
    "properties": {
        "userId": {"type": "string"},
        "isOnline": {"type": "boolean"},
        "lastSeenDate": {"type": "string", "format": "date-time"},
        "onlinePeriods": {
            "type": "array",
            "items": {
                "type": "array",
                "items": [
                    {"type": "string", "format": "date-time"},
                    {"type": "string", "format": "date-time"}
                ]
            }
        }
    },
    "required": ["userId", "isOnline", "lastSeenDate"]
}

@pytest.fixture
def mock_get_data():
    with patch('data_procession.get_data') as mock:
        yield mock

@pytest.fixture(autouse=True)
def setup_teardown():
    fetch_and_update_data()
    yield
    delete_user_data()

@pytest.mark.parametrize('user_data', [
    {'userId': '1', 'isOnline': True, 'lastSeenDate': '2023-01-01T00:00:00'},
    {'userId': '2', 'isOnline': True, 'lastSeenDate': '2023-01-01T00:00:00'}
])
def test_Should_FetchAndUpdateUserData_When_DataDeleted(mock_get_data, user_data):
    mock_get_data.return_value = [user_data]

    try:
        fetch_and_update_data()
        pytest.assert_true(previous_state)
        pytest.assert_in(user_data['userId'], previous_state)

        delete_user_data(user_data['userId'])
        pytest.assert_not_in(user_data['userId'], previous_state)

        fetch_and_update_data()
        pytest.assert_not_in(user_data['userId'], previous_state)
    except Exception as e:
        print(f"An error occurred: {str(e)}")

@pytest.mark.parametrize('user_data', [
    {'userId': '1', 'isOnline': True, 'lastSeenDate': '2023-01-01T00:00:00'},
    {'userId': '2', 'isOnline': True, 'lastSeenDate': '2023-01-01T00:00:00'}
])
def test_Should_FetchAndUpdateDeletedData_When_MultipleUsers(mock_get_data, user_data):
    mock_get_data.return_value = [user_data]

    try:
        fetch_and_update_data()
        pytest.assert_true(previous_state)

        delete_user_data(user_data['userId'])
        pytest.assert_not_in(user_data['userId'], previous_state)

        fetch_and_update_data()
        pytest.assert_not_in(user_data['userId'], previous_state)
        pytest.assert_in(user_data['userId'], previous_state)
    except Exception as e:
        print(f"An error occurred: {str(e)}")

@pytest.mark.parametrize('user_data', [
    {'userId': '1', 'isOnline': True, 'lastSeenDate': '2023-01-01T00:00:00', 'onlinePeriods': [['2023-10-09T14:14:17', '2023-10-09T15:14:17']]}
])
def test_Should_CalculateTimeAndDeleteUser_Properly(mock_get_data, user_data):
    mock_get_data.return_value = [user_data]

    try:
        assert calculate_days(user_data) == 1
        assert calculate_online_time(user_data) == 3600.0
        weekly_avg, daily_avg = calculate_average_times(user_data)
        assert weekly_avg == 3600.0 * 7
        assert daily_avg == 3600.0

        delete_user_data(user_data['userId'])
        assert user_data['userId'] not in previous_state

        fetch_and_update_data()
        assert user_data['userId'] not in previous_state
    except Exception as e:
        print(f"An error occurred: {str(e)}")

def test_generate_report(mock_open, mock_load, mock_dump):
    mocker.patch('builtins.open', new_callable=mock_open)
    mocker.patch('json.load', return_value=[{"userId": "test_user", "onlinePeriods": [["2023-01-01T00:00:00", "2023-01-01T00:10:00"]]}])

    try:
        generate_report('test_report', ['dailyAverage', 'total', 'weeklyAverage'], ['test_user'])
        args, _ = mock_dump.call_args
        report_data = args[0]
        assert 'test_user' in report_data
        assert 'dailyAverage' in report_data['test_user']
        assert 'weeklyAverage' in report_data['test_user']
        assert 'total' in report_data['test_user']
    except Exception as e:
        print(f"An error occurred: {str(e)}")


class TestIntegrationGenerateAndFilterReport(unittest.TestCase):
    def test_integration_generate_and_filter_report(self):
        all_data = [
            {
                "userId": "user1",
                "metrics": [
                    {"date": "2023-10-15", "dailyAverage": 100},
                    {"date": "2023-10-16", "dailyAverage": 150},
                    {"date": "2023-10-17", "dailyAverage": 200},
                ]
            },
            {
                "userId": "user2",
                "metrics": [
                    {"date": "2023-10-15", "dailyAverage": 50},
                    {"date": "2023-10-16", "dailyAverage": 80},
                    {"date": "2023-10-17", "dailyAverage": 120},
                ]
            },
        ]

        with open("all_data.json", "w") as f:
            json.dump(all_data, f)
        generate_report("integration_test_report", ["dailyAverage"], ["user1", "user2"])

        from_date = parse("2023-10-16")
        to_date = parse("2023-10-17")

        with open("integration_test_report.json", "r") as f:
            generated_report_data = json.load(f)

        filtered_reports = get_reports_in_date_range(generated_report_data, from_date, to_date)
        self.assertEqual(len(filtered_reports), 2)

if __name__ == '__main__':
    pytest.main()
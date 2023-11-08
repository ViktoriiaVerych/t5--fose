import pytest
from datetime import datetime, timedelta
import data_procession

from unittest.mock import patch, MagicMock

class TestIntegration:
    @pytest.fixture
    def user_data(self):
        user_id = '1'
        user = {'userId': user_id, 'isOnline': True, 'lastSeenDate': datetime.utcnow().isoformat()}
        return user

    @patch('data_procession.get_data')
    def test_Should_FetchAndUpdateUserData_When_DataDeleted(self, mock_get_data, user_data):
        mock_get_data.return_value = [user_data]

        data_procession.fetch_and_update_data()
        assert data_procession.previous_state
        assert user_data['userId'] in data_procession.previous_state

        data_procession.delete_user_data(user_data['userId'])
        assert user_data['userId'] not in data_procession.previous_state

        data_procession.fetch_and_update_data()
        assert user_data['userId'] not in data_procession.previous_state


    @patch('data_procession.get_data')
    def test_Should_FetchAndUpdateDeletedData_When_MultipleUsers(self, mock_get_data, user_data):
        user1_id = '1'
        user1 = {'userId': user1_id, 'isOnline': True, 'lastSeenDate': datetime.utcnow().isoformat()}
        user2_id = '2'
        user2 = {'userId': user2_id, 'isOnline': True, 'lastSeenDate': datetime.utcnow().isoformat()}
        mock_get_data.return_value = [user1, user2]

        data_procession.fetch_and_update_data()
        assert data_procession.previous_state

        data_procession.delete_user_data(user1_id)
        assert user1_id not in data_procession.previous_state

        data_procession.fetch_and_update_data()
        assert user1_id not in data_procession.previous_state
        assert user2_id in data_procession.previous_state

    @patch('data_procession.get_data')
    def test_Should_CalculateTimeAndDeleteUser_Properly(self, mock_get_data, user_data):
        mock_get_data.return_value = [user_data]

        assert data_procession.calculate_days(user_data) == 1
        assert data_procession.calculate_online_time(user_data) == 3600.0
        weekly_avg, daily_avg = data_procession.calculate_average_times(user_data)
        assert weekly_avg == 3600.0 * 7
        assert daily_avg == 3600.0

        data_procession.delete_user_data(user_data['userId'])
        assert user_data['userId'] not in data_procession.previous_state

        data_procession.fetch_and_update_data()
        assert user_data['userId'] not in data_procession.previous_state


if __name__ == '__main__':
    pytest.main()
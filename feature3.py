import pytest
import data_procession
from datetime import datetime

@pytest.mark.parametrize("user_id, expected_data", [
    ('1', [{'userId': '2'}]),
    ('3', [{'userId': '1'}, {'userId': '2'}]),
    (None, [{'userId': '1'}, {'userId': '2'}]),
    ('1', []),
])
def test_delete_user_data(user_id, expected_data):
    with patch('json.dump') as mock_dump, \
            patch('json.load') as mock_load, \
            patch('builtins.open') as mock_open:
        mock_load.return_value = [{'userId': '1'}, {'userId': '2'}]
        data_procession.delete_user_data(user_id)
        mock_dump.assert_called_once_with(expected_data, mock_open.return_value.__enter__.return_value)
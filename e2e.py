import os
import pytest
import requests
import json

BASE_URL = os.environ.get('BASE_URL', 'http://123.0.0.1:5000')
DATA = {
    "metrics": ["dailyAverage", "total", "weeklyAverage"],
    "users": [
        "db58d6ab-73cb-40fe-819d-ef4f851c74b9",
        "961038b5-3b9b-415b-9bae-cf0634ddcad8",
        "61b26e2c-a0d1-4461-aa80-13241ec292e1",
    ]
}

def test_generate_report_endpoint():
    report_name = "test_report"
    url = f'{BASE_URL}/api/report/{report_name}'

    response = requests.post(url, json=DATA)

    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert data["message"] == f"Report '{report_name}' successfully created."

if __name__ == "__main__":
    pytest.main([__file__])
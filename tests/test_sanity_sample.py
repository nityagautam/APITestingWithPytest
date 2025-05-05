from unittest.mock import MagicMock, Mock
import pytest


class TestSampleAPITest:
    """
    Sample test class
    """

    def test_sample(self):
        """
        Sample test
        """
        assert True, "Sample test failed"

    def test_mock(self):
        """
        Sample test with mock
        """
        mock = MagicMock()
        mock.return_value = 42
        assert mock() == 42, "Mock test failed"

    def test_invalid_user(self, api_client):
        """
        Test invalid user
        """
        response = api_client.get("/invalid_user")
        assert response.status_code == 404, "Expected 404 for invalid user"
        assert response.json() == {"error": "User not found"}, "Expected error message for invalid user"

    def test_valid_user(self, api_client):
        """
        Test valid user
        """
        response = api_client.get("/valid_user")
        assert response.status_code == 200, "Expected 200 for valid user"
        assert response.json() == {"user": "valid_user"}, "Expected user data for valid user" 
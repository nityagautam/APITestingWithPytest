from unittest.mock import MagicMock, Mock
from jsonschema import validate
import requests
import responses
import pytest


class TestSampleAPITest:
    """
    Sample test class
    """

    # User data
    # ----------------------
    # expected schema
    user_schema = {
        "type": "object",
        "required": ["id", "name", "email"],
        "properties": {
            "id": {"type": "integer"},
            "name": {"type": "string"},
            "email": {"type": "string", "format": "email"},
        }
    }

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

    @pytest.mark.parametrize("user_id", [1, 2, 3])
    def test_get_user(self, api_client, user_id):
        response = api_client.get(f"/users/{user_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == user_id
        assert "email" in data

    # Schema Validation Testing for multiple users
    @pytest.mark.parametrize("user_id", [1, 2, 3])
    def test_user_schema_validation(self, api_client, user_id):
        response = api_client.get(f"/users/{user_id}")
        assert response.status_code == 200
        data = response.json()

        
        # Validate response against schema
        # validate(instance=data, schema=user_schema)
        try:
            validate(instance=data, schema=self.user_schema)
        except ValidationError as e:
            pytest.fail(f"Schema validation failed: {e.message}")



    # --------------------------
    # Mock Testing
    # --------------------------
    @responses.activate
    def test_mock_api_response_with_schema(self, api_client):
        url = "https://fakeapi.com/users/1"
        mock_data = {
            "id": 1,
            "name": "Alice",
            "email": "alice@example.com"
        }

        responses.add(responses.GET, url, json=mock_data, status=200)
        response = requests.get("https://fakeapi.com/users/1")
        validate(instance=response.json(), schema=self.user_schema)
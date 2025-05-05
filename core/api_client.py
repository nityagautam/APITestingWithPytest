import pytest
import requests

class APIClient:
    def __init__(self, base_url, auth_token=None):
        self.base_url = base_url
        print(f"Given Base URL: {self.base_url}")
        self.headers = {
            "Content-Type": "application/json"
        }
        if auth_token:
            self.headers["Authorization"] = f"Bearer {auth_token}"

    def get(self, endpoint, params=None):
        try:
            return requests.get(f"{self.base_url}{endpoint}", headers=self.headers, params=params)
        except requests.exceptions.RequestException as e:
            print(f"Failed to connect to {self.base_url}{endpoint}: {e}")

    def post(self, endpoint, data=None):
        return requests.post(f"{self.base_url}{endpoint}", headers=self.headers, json=data)

    def put(self, endpoint, data=None):
        return requests.put(f"{self.base_url}{endpoint}", headers=self.headers, json=data)

    def delete(self, endpoint):
        return requests.delete(f"{self.base_url}{endpoint}", headers=self.headers)
import unittest
import requests


BASE_URL = "http://demo-fastapi-app.openfactory.local"


class TestFastAPIEndpoints(unittest.TestCase):
    """
    Test endpoints of an OpenFactoryFastAPI App
    """

    def test_root_endpoint(self):
        response = requests.get(f"{BASE_URL}/")
        print(response.content)

        self.assertEqual(response.status_code, 200)

        data = response.json()
        self.assertIn("status", data)

    def test_move_endpoint(self):
        payload = {
            "x": 1.5,
            "y": 2.5
        }

        response = requests.post(f"{BASE_URL}/move", params=payload)

        self.assertEqual(response.status_code, 200)

        data = response.json()
        self.assertEqual(data.get("message"), "moving")

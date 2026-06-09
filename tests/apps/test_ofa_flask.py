import unittest
import requests


BASE_URL = "http://demo-flask-app.openfactory.local"


class TestFastAPIEndpoints(unittest.TestCase):
    """
    Test endpoints of an OpenFactoryFlask App
    """

    def test_root_endpoint(self):
        response = requests.get(f"{BASE_URL}/")
        self.assertEqual(response.status_code, 200)

        html = response.text
        self.assertIn("<title>OpenFactory Flask App</title>", html)
        self.assertIn("<h1>Hello World</h1>", html)
        self.assertIn("Welcome to OpenFactory Flask App", html)

    def test_url_for_generates_expected_about_link(self):
        """ Test if url_for computes corret link """
        response = requests.get(f"{BASE_URL}/")
        self.assertEqual(response.status_code, 200)
        html = response.text
        self.assertIn(
            '<a href="/about">About</a>',
            html
        )

    def test_about_endpoint(self):
        response = requests.get(f"{BASE_URL}/about")
        self.assertEqual(response.status_code, 200)

        html = response.text
        self.assertIn("About OpenFactory Flask App", html)

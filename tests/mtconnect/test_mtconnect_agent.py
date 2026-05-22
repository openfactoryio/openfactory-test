import unittest
import requests


BASE_URL = "http://mtconnect-temp-sens.agent.openfactory.local"


class TestMTConnectAgent(unittest.TestCase):
    """
    Test if MTCOnnect agent is deployed as expected
    """

    def test_root_endpoint(self):
        response = requests.get(f"{BASE_URL}/")
        self.assertEqual(response.status_code, 200)

        self.assertIn("xml", response.headers["Content-Type"])
        xml = response.text

        # Verify this is an MTConnectDevices document
        self.assertIn("<MTConnectDevices", xml)

        # Verify expected virtual device exists
        self.assertIn('name="VIRTUAL-TEMPERATURE-SENSOR"', xml)

        # Verify expected temperature data item exists
        self.assertIn('type="TEMPERATURE"', xml)

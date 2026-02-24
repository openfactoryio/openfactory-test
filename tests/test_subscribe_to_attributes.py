import os
import threading
from unittest import TestCase

from openfactory.kafka import KSQLDBClient
from openfactory.assets import Asset


class TestSendCmds(TestCase):
    """
    Test subscriptions to Assets
    """

    @classmethod
    def setUpClass(cls):
        cls.ksql = KSQLDBClient(os.getenv("KSQLDB_URL"))

        cls.temp_sensor = Asset(
            'OPCUA-SENSOR-001',
            ksqlClient=cls.ksql,
            bootstrap_servers=os.getenv("KAFKA_BROKER")
        )

    @classmethod
    def tearDownClass(cls):
        cls.ksql.close()

    def test_subscribe_to_attribute(self):
        """ Test that subscribing to temp attribute receives at least one sample. """

        message_received = threading.Event()
        received_payload = {}

        def on_sample(msg_key, msg_value):
            nonlocal received_payload
            received_payload = msg_value
            message_received.set()

        # Subscribe
        self.temp_sensor.subscribe_to_attribute('temp', on_sample)

        # Wait max 5 seconds for first message
        received = message_received.wait(timeout=5)

        self.assertTrue(
            received,
            "Did not receive any temperature sample within 5 seconds"
        )

        # Minimal structural validation (not checking exact values)
        self.assertIn("VALUE", received_payload)
        self.assertIn("TYPE", received_payload)
        self.assertEqual(received_payload["TYPE"], "Samples")

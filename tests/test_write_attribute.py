import os
from unittest import TestCase

from openfactory.kafka import KSQLDBClient
from openfactory.assets import Asset


class TestSendCmds(TestCase):
    """
    Tests related to send OpenFactory commands to Assets
    """

    @classmethod
    def setUpClass(cls):
        # setup link to ksqlDB
        cls.ksql = KSQLDBClient(os.getenv("KSQLDB_URL"))

        # setup Assets
        cls.temp_sensor = Asset(
            'OPCUA-SENSOR-001',
            ksqlClient=cls.ksql,
            bootstrap_servers=os.getenv("KAFKA_BROKER"))

    @classmethod
    def tearDownClass(cls):
        cls.ksql.close()

    def test_write_attribute(self):
        """ Test if attribute can be written. """
        self.temp_sensor.temp_unit = 'K'

        # Wait until the asset reports new temperature unit
        result = self.temp_sensor.wait_until("temp_unit", "K", 5)

        self.assertTrue(
            result,
            "Temperature sensor did not switch to 'K' units within 5 seconds"
        )

        self.temp_sensor.temp_unit = 'C'

        # Wait until the asset reports new temperature unit
        result = self.temp_sensor.wait_until("temp_unit", "C", 5)

        self.assertTrue(
            result,
            "Temperature sensor did not switch to 'C' units within 5 seconds"
        )

import os
from unittest import TestCase
from openfactory.kafka import KSQLDBClient
from openfactory.assets import Asset


class TestMTConnectDevice(TestCase):
    """
    Tests if the MTConnect Device was deployed as expected
    """

    @classmethod
    def setUpClass(cls):
        # setup link to ksqlDB
        cls.ksql = KSQLDBClient(os.getenv("KSQLDB_URL"))

        # setup Asset
        cls.device = Asset(
            'MTCONNECT-TEMP-SENS',
            ksqlClient=cls.ksql,
            bootstrap_servers=os.getenv("KAFKA_BROKER"))

    @classmethod
    def tearDownClass(cls):
        cls.ksql.close()

    def test_avail(self):
        """ Test app is AVAILABLE """
        self.assertEqual(self.device.avail.value, 'AVAILABLE')

    def test_temperature(self):
        """ Test Temp attribute """
        self.assertNotEqual(self.device.Temp.value, 'UNAVAILABLE')
        self.assertNotEqual(self.device.Temp.tag, 'Temperature')
        self.assertNotEqual(self.device.Temp.type, 'Sample')

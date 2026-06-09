import os
from unittest import TestCase
from openfactory.kafka import KSQLDBClient
from openfactory.assets import Asset


class TestSHDRDevice(TestCase):
    """
    Tests if the SHDR Device was deployed as expected
    """

    @classmethod
    def setUpClass(cls):
        # setup link to ksqlDB
        cls.ksql = KSQLDBClient(os.getenv("KSQLDB_URL"))

        # setup Asset
        cls.device = Asset(
            'VIRTUAL-SHDR-SENS',
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
        self.assertEqual(self.device.Temp.tag, 'Temperature')
        self.assertEqual(self.device.Temp.type, 'Samples')

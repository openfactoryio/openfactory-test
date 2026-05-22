import os
from unittest import TestCase
from openfactory.kafka import KSQLDBClient
from openfactory.assets import Asset


class TestMTConnectProducer(TestCase):
    """
    Tests if the MTConnect Producer was deployed as expected
    """

    @classmethod
    def setUpClass(cls):
        # setup link to ksqlDB
        cls.ksql = KSQLDBClient(os.getenv("KSQLDB_URL"))

        # setup Asset
        cls.producer = Asset(
            'MTCONNECT-TEMP-SENS-PRODUCER',
            ksqlClient=cls.ksql,
            bootstrap_servers=os.getenv("KAFKA_BROKER"))

    @classmethod
    def tearDownClass(cls):
        cls.ksql.close()

    def test_avail(self):
        """ Test app is AVAILABLE """
        self.assertEqual(self.producer.avail.value, 'AVAILABLE')

import os
from unittest import TestCase
from openfactory.kafka import KSQLDBClient
from openfactory.assets import Asset


class TestAttributesOpenFactoryApp(TestCase):
    """
    Tests related to execute OpenFactory commands in OpenFactory Apps
    """

    @classmethod
    def setUpClass(cls):
        # setup link to ksqlDB
        cls.ksql = KSQLDBClient(os.getenv("KSQLDB_URL"))

        # setup Asset
        cls.app = Asset(
            'DEMO-APP',
            ksqlClient=cls.ksql,
            bootstrap_servers=os.getenv("KAFKA_BROKER"))

    @classmethod
    def tearDownClass(cls):
        cls.ksql.close()

    def test_avail(self):
        """ Test app is AVAILABLE """
        self.assertEqual(self.app.avail.value, 'AVAILABLE')

    def test_declarative_attributes(self):
        """ Test if decalrative attributes exist """
        self.assertIn('x', self.app.attributes())
        self.assertIn('y', self.app.attributes())
        self.assertIn('speed', self.app.attributes())
        self.assertIn('barcode', self.app.attributes())

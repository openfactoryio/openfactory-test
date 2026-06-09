import os
from unittest import TestCase
from openfactory.kafka import KSQLDBClient
from openfactory.assets import Asset


class TestAssetSubscription(TestCase):
    """
    Tests related to subsription between Assets
    """

    @classmethod
    def setUpClass(cls):
        # setup link to ksqlDB
        cls.ksql = KSQLDBClient(os.getenv("KSQLDB_URL"))

        # setup Assets
        cls.app = Asset(
            'DEMO-APP',
            ksqlClient=cls.ksql,
            bootstrap_servers=os.getenv("KAFKA_BROKER"))

        cls.barcode_reader = Asset(
            'VIRTUAL-BARCODE-READER',
            ksqlClient=cls.ksql,
            bootstrap_servers=os.getenv("KAFKA_BROKER"))

    @classmethod
    def tearDownClass(cls):
        cls.ksql.close()

    def test_asset_subscription(self):
        """ Test DEMO-APP is correctly subscribing to VIRTUAL-BARCODE-READER """

        # Sets barcode reader to MANUAL mode and generate a specific code
        self.barcode_reader.SetManualMode(sender_uuid='TEST')
        result = self.barcode_reader.wait_until("simulation_mode", "MANUAL", 5, use_ksqlDB=True)
        self.assertTrue(
            result,
            "Barcode reader did not switch to MANUAL mode within 5 seconds"
        )

        self.barcode_reader.GenerateCode(sender_uuid='TEST', Code='TEST-BARCODE')
        result = self.barcode_reader.wait_until("last_code", "TEST-BARCODE", 5, use_ksqlDB=True)
        self.assertTrue(
            result,
            "Barcode reader did not report new barcode within 5 seconds"
        )

        # Test that DEMO-APP did correctly get generated barcode via its subscription
        result = self.app.wait_until("barcode", "TEST-BARCODE", 5, use_ksqlDB=True)
        self.assertTrue(
            result,
            "DEMO-APP did not report new barcode within 5 seconds"
        )

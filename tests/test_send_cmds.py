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

        cls.barcode_reader = Asset(
            'VIRTUAL-BARCODE-READER',
            ksqlClient=cls.ksql,
            bootstrap_servers=os.getenv("KAFKA_BROKER"))

    @classmethod
    def tearDownClass(cls):
        cls.ksql.close()

    def test_methods_dicovery(self):
        """ Tests if assets exposes correctly methods. """

        expected_temp_sensor_methods = {
            "Calibrate": {
                "description": "Calibrate",
                "arguments": []
            }
        }

        expected_barcode_reader_methods = {
            "GenerateCode": {
                "description": "GenerateCode",
                "arguments": [
                    {
                        "name": "Code",
                        "description": "Barcode to generate (empty for random)"
                    }
                ]
            },
            "SetAutomaticMode": {
                "description": "SetAutomaticMode",
                "arguments": []
            },
            "SetManualMode": {
                "description": "SetManualMode",
                "arguments": []
            }
        }

        self.assertEqual(
            self.temp_sensor.methods(),
            expected_temp_sensor_methods,
            "Temp sensor methods mismatch"
        )

        self.assertEqual(
            self.barcode_reader.methods(),
            expected_barcode_reader_methods,
            "Barcode reader methods mismatch"
        )

    def test_method_execution(self):
        """ Test if methods get executed """
        self.barcode_reader.SetManualMode(sender_uuid='TEST')

        # Wait until the asset reports MANUAL mode
        result = self.barcode_reader.wait_until("simulation_mode", "MANUAL", 5, use_ksqlDB=True)

        self.assertTrue(
            result,
            "Barcode reader did not switch to MANUAL mode within 5 seconds"
        )

        self.barcode_reader.GenerateCode(sender_uuid='TEST', Code='MANUAL-BARCODE')

        # Wait until the asset reports new barcode
        result = self.barcode_reader.wait_until("last_code", "MANUAL-BARCODE", 5, use_ksqlDB=True)

        self.assertTrue(
            result,
            "Barcode reader did not report new barcode within 5 seconds"
        )

        self.barcode_reader.SetAutomaticMode(sender_uuid='TEST')

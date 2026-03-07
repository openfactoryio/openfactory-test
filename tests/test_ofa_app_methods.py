import os
from unittest import TestCase
from openfactory.kafka import KSQLDBClient
from openfactory.assets import Asset


class TestRunCmdsOpenFactoryApp(TestCase):
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

    def test_execute_cmd(self):
        """ Executes some commands """

        # excecute move_axis method on DEMO-APP
        self.app.move_axis(sender_uuid='test-uuid', x='10', y='-5')

        # make sure new values are sent to full OpenFacotry pipeline (can take some ms)
        self.app.wait_until("x", 10, timeout=1, use_ksqlDB=True)
        self.app.wait_until("y", -5, timeout=1, use_ksqlDB=True)
        self.app.wait_until("speed", 100, timeout=1, use_ksqlDB=True)

        self.assertEqual(self.app.x.value, 10)
        self.assertEqual(self.app.y.value, -5)
        self.assertEqual(self.app.speed.value, 100)

        # excecute stop_axis method on DEMO-APP
        self.app.stop_axis(sender_uuid='test-uuid')

        # make sure new values are sent to full OpenFacotry pipeline
        self.app.wait_until("speed", 0, timeout=1, use_ksqlDB=True)

        self.assertEqual(self.app.speed.value, 0)

    def test_execute_invalid_cmd(self):
        """ Tests that a command with none-valid arguments is not executed """
        # Make sure speed = 0
        self.app.stop_axis(sender_uuid='test-uuid')
        self.app.wait_until("speed", 0, timeout=1, use_ksqlDB=True)

        # Try to execute a command with none valid arguments (here missing equired y argument)
        self.app.move_axis(sender_uuid='test-uuid', x='10', speed='50')

        # Check speed never gets set to 50
        result = self.app.wait_until("speed", 50, timeout=1, use_ksqlDB=True)
        self.assertFalse(result)

    def test_retrieve_methods_info(self):
        """ Test available methods in DEMO-APP """
        methods = self.app.methods()

        self.assertIn('move_axis', methods)
        self.assertEqual(methods['move_axis']['description'], 'Move to a given (x, y) position with speed')
        expected_arguments = [
            {'name': 'x', 'description': 'X coordinate'},
            {'name': 'y', 'description': 'Y coordinate'},
            {'name': 'speed', 'description': 'Feed rate (optional; defaults to 100)'}]
        self.assertEqual(methods['move_axis']['arguments'], expected_arguments)

        self.assertIn('stop_axis', methods)
        self.assertEqual(methods['stop_axis']['description'], 'Stops all motion immediately.')

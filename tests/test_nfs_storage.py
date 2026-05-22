import os
from unittest import TestCase
from openfactory.kafka import KSQLDBClient
from openfactory.assets import Asset


class TestNFStorage(TestCase):
    """
    Tests if OpenFactory Apps can mount as expected NFS storage
    """

    @classmethod
    def setUpClass(cls):
        # setup link to ksqlDB
        cls.ksql = KSQLDBClient(os.getenv("KSQLDB_URL"))

        # setup Assets
        cls.app1 = Asset(
            'DEMO-APP',
            ksqlClient=cls.ksql,
            bootstrap_servers=os.getenv("KAFKA_BROKER"))
        cls.app2 = Asset(
            'DEMO-APP2',
            ksqlClient=cls.ksql,
            bootstrap_servers=os.getenv("KAFKA_BROKER"))

    @classmethod
    def tearDownClass(cls):
        cls.app1.close()
        cls.app2.close()
        cls.ksql.close()

    def test_avail(self):
        """ Test apps are AVAILABLE """
        self.assertEqual(self.app1.avail.value, 'AVAILABLE')
        self.assertEqual(self.app2.avail.value, 'AVAILABLE')

    def test_rw_nfs_storage_mounted(self):
        """ Test that a rw NFS storage is mounted in rw mode """
        self.assertEqual(self.app1.file_error.value, 'UNAVAILABLE')

    def test_ro_nfs_storage_mounted(self):
        """ Test that a ro NFS storage is mounted in ro mode """
        self.assertEqual(self.app2.file_error.value, "[Errno 30] Read-only file system: '/mnt/test_folder_DEMO-APP2'")

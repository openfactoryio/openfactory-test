import os
import threading
from datetime import datetime, timezone
from unittest import TestCase

from openfactory.assets import Asset
from openfactory.kafka import KSQLDBClient


class TestLatency(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.ksql = KSQLDBClient(os.getenv("KSQLDB_URL"))
        cls.asset = Asset(
            'OPCUA-SENSOR-001',
            ksqlClient=cls.ksql,
            bootstrap_servers=os.getenv("KAFKA_BROKER")
        )

    @classmethod
    def tearDownClass(cls):
        cls.ksql.close()

    def test_sample_latency_below_30ms(self):
        """
        Ensure sample ingestion latency is below 30ms.
        """

        latencies = []
        sample_received = threading.Event()

        def on_sample(msg_subject, msg_value):

            msg_ts = msg_value['attributes']['timestamp']
            msg_time = datetime.fromisoformat(msg_ts.replace('Z', '+00:00'))
            now_time = datetime.now(timezone.utc)

            delta = (now_time - msg_time).total_seconds()
            latencies.append(delta)

            # Stop after collecting 5 samples
            if len(latencies) >= 5:
                sample_received.set()

        self.asset.subscribe_to_samples(on_sample)

        # Wait max 10 seconds to collect samples
        received = sample_received.wait(timeout=10)

        self.assertTrue(
            received,
            "Did not receive enough samples within timeout"
        )

        # Convert to milliseconds
        latencies_ms = [la * 1000 for la in latencies]

        max_latency = max(latencies_ms)

        self.assertLess(
            max_latency,
            30,
            f"Latency too high: max observed {max_latency:.2f} ms"
        )

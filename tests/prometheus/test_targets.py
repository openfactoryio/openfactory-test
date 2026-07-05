import json
import unittest
import urllib.request


class TestPrometheusTargets(unittest.TestCase):
    PROMETHEUS_URL = "http://localhost:9090"

    EXPECTED_TARGETS = {
        "asset_forwarder:4000",
        "opcua-coordinator:4000",
        "opcua-gateway-1:4000",
        "opcua-gateway-2:4000",
        "shdr-coordinator:4000",
        "shdr-gateway-1:4000",
        "shdr-gateway-2:4000",
        "demo-fastapi-app:5000",
    }

    def test_openfactory_targets_are_up(self):
        with urllib.request.urlopen(f"{self.PROMETHEUS_URL}/api/v1/targets") as response:
            data = json.load(response)

        targets = {
            t["labels"]["instance"]: t
            for t in data["data"]["activeTargets"]
            if t["labels"].get("job") == "openfactory"
        }

        # Verify all expected targets are present.
        self.assertEqual(
            set(targets.keys()),
            self.EXPECTED_TARGETS,
            f"Unexpected targets.\n"
            f"Expected: {sorted(self.EXPECTED_TARGETS)}\n"
            f"Found:    {sorted(targets.keys())}",
        )

        # Verify each target is healthy.
        unhealthy = [
            instance
            for instance, target in targets.items()
            if target["health"] != "up"
        ]

        self.assertEqual(
            unhealthy,
            [],
            f"Targets not healthy: {', '.join(unhealthy)}",
        )

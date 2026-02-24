import os
import json
from uuid import uuid4
from datetime import datetime, timezone
import openfactory.config as config
from openfactory.assets import Asset
from openfactory.kafka import KSQLDBClient
from openfactory.schemas.command_header import CommandEnvelope, CommandHeader

ksql = KSQLDBClient(config.KSQLDB_URL)

# Example 1: temp sensor
temp_sensor = Asset('OPCUA-SENSOR-001', ksqlClient=ksql, bootstrap_servers=os.getenv("KAFKA_BROKER"))
print(json.dumps(temp_sensor.methods()))
print("Requesting Calibrate method ...")
envelope = CommandEnvelope(
    header=CommandHeader(
        correlation_id=uuid4(),
        sender_uuid="TEST-HMI",
        timestamp=datetime.now(timezone.utc),
        signature=None
    ),
    arguments={}
)
temp_sensor.Calibrate_CMD = envelope.model_dump_json()

# Example 2: barcode reader - SetManualMode
barcode_reader = Asset('VIRTUAL-BARCODE-READER', ksqlClient=ksql, bootstrap_servers=config.KAFKA_BROKER)
print(json.dumps(barcode_reader.methods()))
print(barcode_reader.methods()["GenerateCode"]["arguments"][0]['name'])

barcode_reader.SetManualMode(sender_uuid='TEST')
barcode_reader.GenerateCode(sender_uuid='SENDER-ID', Code='MANUAL-BARCODE')

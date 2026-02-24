import os
import json
import openfactory.config as config
from openfactory.assets import Asset
from openfactory.kafka import KSQLDBClient

ksql = KSQLDBClient(config.KSQLDB_URL)

# Example 1: temp sensor
temp_sensor = Asset('OPCUA-SENSOR-001', ksqlClient=ksql, bootstrap_servers=os.getenv("KAFKA_BROKER"))
print(json.dumps(temp_sensor.methods()))
print("Requesting Calibrate method ...")
temp_sensor.Calibrate(sender_uuid='TEST')

# Example 2: barcode reader - SetManualMode
barcode_reader = Asset('VIRTUAL-BARCODE-READER', ksqlClient=ksql, bootstrap_servers=config.KAFKA_BROKER)
print(json.dumps(barcode_reader.methods()))
print(barcode_reader.methods()["GenerateCode"]["arguments"][0]['name'])

barcode_reader.SetManualMode(sender_uuid='TEST')
barcode_reader.GenerateCode(sender_uuid='SENDER-ID', Code='MANUAL-BARCODE')

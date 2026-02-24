import os
import time
import openfactory.config as config
from openfactory import OpenFactory
from openfactory.assets import Asset
from openfactory.kafka import KSQLDBClient

# --- Setup ---
ksql = KSQLDBClient(config.KSQLDB_URL)
ofa = OpenFactory(ksqlClient=KSQLDBClient(config.KSQLDB_URL))

asset = Asset(
    'OPCUA-SENSOR-001',
    ksqlClient=ksql,
    bootstrap_servers=os.getenv("KAFKA_BROKER"))

print(asset.temp)
print(asset.temp_unit)

asset.temp_unit = 'K'
time.sleep(0.1)

print(asset.temp_unit)

def on_sample(msg_key, msg_value):
    print(msg_key, msg_value['VALUE'])
    print(msg_value)

asset.subscribe_to_attribute('temp', on_sample)

time.sleep(10)

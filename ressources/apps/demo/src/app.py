import time
import os
from openfactory.apps import OpenFactoryApp
from openfactory.kafka import KSQLDBClient


class DemoApp(OpenFactoryApp):

    def main_loop(self):
        self.logger.info("I don't do anything useful in this example.")
        counter = 1
        while True:
            print(counter)
            counter += 1
            time.sleep(2)

    def app_event_loop_stopped(self):
        # Not absolutely required as it is already done by the `KSQLDBClient` class
        self.ksql.close()

app = DemoApp(
    ksqlClient=KSQLDBClient(os.getenv("KSQLDB_URL", "http://localhost:8088")),
    bootstrap_servers=os.getenv("KAFKA_BROKER", "localhost:9092"),
    loglevel=os.getenv("LOG_LEVEL", "INFO")
)
app.run()

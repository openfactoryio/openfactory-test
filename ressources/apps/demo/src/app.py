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
        self.ksql.close()


app = DemoApp(
    ksqlClient=KSQLDBClient(os.getenv("KSQLDB_URL")),
    bootstrap_servers=os.getenv("KAFKA_BROKER"),
    loglevel=os.getenv("LOG_LEVEL")
)
app.run()

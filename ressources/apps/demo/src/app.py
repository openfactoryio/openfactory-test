import time
import os
from typing import Annotated
from openfactory.apps import OpenFactoryApp, SampleAttribute, EventAttribute, ofa_method
from openfactory.kafka import KSQLDBClient
from openfactory.assets import Asset


class DemoApp(OpenFactoryApp):

    x = SampleAttribute(value=0, tag="Position")
    y = SampleAttribute(value=0, tag="Position")
    speed = SampleAttribute(value=0, tag="FeedRate")
    barcode = EventAttribute(tag="Barcode")

    def __init__(self,
                 ksqlClient: KSQLDBClient,
                 loglevel: str):
        """ Constructor """
        super().__init__(ksqlClient=ksqlClient,
                         loglevel=loglevel)

        # subscribe to another Asset
        barcode_reader = Asset('VIRTUAL-BARCODE-READER', ksqlClient=ksqlClient)
        barcode_reader.subscribe_to_attribute('last_code', self.on_new_barcode)

    @ofa_method(description="Move to a given (x, y) position with speed")
    def move_axis(
            self,
            x: Annotated[float, "X coordinate"],
            y: Annotated[float, "Y coordinate"],
            speed: Annotated[int, "Feed rate (optional; defaults to 100)"] = 100):
        self.logger.info(f"Moving axis to x={x}, y={y} at speed={speed}")
        self.x = x
        self.y = y
        self.speed = speed

    @ofa_method()
    def stop_axis(self):
        """ Stops all motion immediately. """
        self.logger.info("Stopping all axis")
        self.speed = 0

    def on_new_barcode(self, msg_key, msg_value):
        """ Called on each new read of the VIRTUAL-BARCODE-READER """
        print(msg_value['VALUE'])
        self.barcode = msg_value['VALUE']

    def main_loop(self):
        self.logger.info("I don't do anything useful in this example.")
        counter = 1
        while True:
            print(counter)
            counter += 1
            time.sleep(10)

    def app_event_loop_stopped(self):
        self.ksql.close()


app = DemoApp(
    ksqlClient=KSQLDBClient(os.getenv("KSQLDB_URL")),
    loglevel=os.getenv("LOG_LEVEL")
)
app.run()

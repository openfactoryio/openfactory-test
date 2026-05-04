import asyncio
import os
from typing import Annotated

from openfactory.apps import OpenFactoryFastAPIApp, ofa_method, EventAttribute, SampleAttribute
from openfactory.kafka import KSQLDBClient
from routes import root, move


class DemoFastAPIApp(OpenFactoryFastAPIApp):

    status = EventAttribute(value="idle", tag="App.Status")
    temperature = SampleAttribute(tag="Temperature")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # expose OFA app inside FastAPI
        self.api.state.ofa_app = self

        # include routers
        self.api.include_router(root.router)
        self.api.include_router(move.router)

    @ofa_method(description="Move axis")
    def move_axis(
        self,
        x: Annotated[float, "X"],
        y: Annotated[float, "Y"]
    ):
        self.logger.info(f"Move to {x},{y}")

    async def async_main_loop(self):
        while True:
            await asyncio.sleep(3)
            self.logger.info("Working hard ...")


app = DemoFastAPIApp(
    ksqlClient=KSQLDBClient(os.getenv("KSQLDB_URL")),
    bootstrap_servers=os.getenv("KAFKA_BROKER"),
    loglevel=os.getenv("LOG_LEVEL", "INFO")
)

app.run()

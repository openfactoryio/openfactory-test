import asyncio
import os
from openfactory.apps.ofa_flask_app import OpenFactoryFlaskApp
from openfactory.kafka import KSQLDBClient
from routes import root_bp, about_bp


class DemoFlaskApp(OpenFactoryFlaskApp):

    def configure_routes(self):
        self.app.register_blueprint(root_bp)
        self.app.register_blueprint(about_bp)

    async def async_main_loop(self):
        counter = 0
        while True:
            counter += 1
            self.logger.info(f"Counter={counter}")
            await asyncio.sleep(5)


app = DemoFlaskApp(
    ksqlClient=KSQLDBClient(os.getenv("KSQLDB_URL")),
    bootstrap_servers=os.getenv("KAFKA_BROKER"),
    loglevel=os.getenv("LOG_LEVEL", "INFO")
)

app.run()

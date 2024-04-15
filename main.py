import asyncio
import sys
import os

from PyQt6.QtWidgets import QApplication
from loguru import logger

from database.mongodb_client import MongoDBClient
from websocket_client.client import WebSocketClient
from data_handler.handler import DataHandler
from ui.main_window import MainWindow

log_directory = os.path.join(os.path.expanduser("~"), "CryptoPriceTrackerLogs")
os.makedirs(log_directory, exist_ok=True)

logger.add(
    f"{log_directory}/app_{{time}}.log",
    rotation="10 MB",
    retention="10 days",
    level="INFO",
)


class CryptoPriceApp:
    def __init__(self) -> None:
        self._log = logger.bind(name="CryptoPriceApp")
        self._app = QApplication([])

        self._mongodb_client = MongoDBClient()
        self._mongodb_client.start()

        self._websocket_client = WebSocketClient()
        self._data_handler = DataHandler()

        self._main_window = MainWindow()
        self._main_window.show()

        self._setup_connections()

    def _setup_connections(self) -> None:
        self._websocket_client.raw_price_update_signal.connect(
            self._data_handler.handle_data
        )
        self._data_handler.processed_price_update_signal.connect(
            self._main_window.update_price_widgets
        )
        self._data_handler.processed_price_update_signal.connect(
            lambda data: asyncio.run_coroutine_threadsafe(
                self._mongodb_client.store_price_data(data), self._mongodb_client.loop
            )
        )

    def start(self) -> None:
        self._websocket_client.start()
        sys.exit(self._app.exec())


if __name__ == "__main__":
    try:
        crypto_app = CryptoPriceApp()
        crypto_app.start()
    except KeyboardInterrupt:
        print("Exiting...")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

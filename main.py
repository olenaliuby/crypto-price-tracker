import sys
import asyncio
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QThread
from loguru import logger

from database.mongodb_client import MongoDBClient
from websocket_client.client import WebSocketClient
from data_handler.handler import DataHandler
from ui.main_window import MainWindow


logger.add("logs/app_{time}.log", rotation="10 MB", retention="10 days", level="INFO")


class AsyncioThread(QThread):
    def __init__(self, loop: asyncio.AbstractEventLoop) -> None:
        super().__init__()
        self.loop = loop

    def run(self) -> None:
        self.loop.run_forever()


class CryptoPriceApp:
    def __init__(self) -> None:
        self._log = logger.bind(name="CryptoPriceApp")
        self.app = QApplication([])

        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)

        self.asyncio_thread = AsyncioThread(self.loop)

        self.websocket_client = WebSocketClient()
        self.data_handler = DataHandler()
        self.mongodb_client = MongoDBClient()
        self.main_window = MainWindow()

    def setup_connections(self) -> None:
        self.websocket_client.price_update.connect(self.data_handler.handle_data)
        self.data_handler.price_update_signal.connect(
            self.main_window.update_price_widgets
        )
        self.data_handler.price_update_signal.connect(
            lambda data: asyncio.run_coroutine_threadsafe(
                self.mongodb_client.store_price_data(data), self.loop
            )
        )

    def start(self) -> None:
        self.asyncio_thread.start()
        self.main_window.show()
        self.setup_connections()
        self.websocket_client.start()
        sys.exit(self.app.exec())


if __name__ == "__main__":
    try:
        crypto_app = CryptoPriceApp()
        crypto_app.start()
    except KeyboardInterrupt:
        print("Exiting...")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

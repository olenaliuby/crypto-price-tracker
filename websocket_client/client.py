import json

from loguru import logger
from PyQt6.QtCore import QThread, pyqtSignal
from websocket import WebSocketApp, WebSocket

from utils.coins import CRYPTO_COINS


class WebSocketClient(QThread):
    price_update = pyqtSignal(dict)

    def __init__(self) -> None:
        super().__init__()
        self._coins = CRYPTO_COINS
        self._streams = "/".join(self._coins.values())
        self._url = f"wss://fstream.binance.com/stream?streams={self._streams}"
        self._log = logger.bind(name="WebSocketClient")

    def run(self) -> None:
        try:
            ws = WebSocketApp(
                self._url,
                on_message=self.on_message,
                on_error=self.on_error,
                on_close=self.on_close,
            )
            ws.on_open = self.on_open
            ws.run_forever()
        except Exception as e:
            self._log.error(f"Error connecting to WebSocket: {e}")

    def on_message(self, ws: WebSocket, message: str) -> None:
        try:
            trade_info = json.loads(message)
            self.price_update.emit(trade_info)  # noqa
        except json.JSONDecodeError as e:
            self._log.error(f"Error decoding message: {e}")

    def on_error(self, ws, error) -> None:
        self._log.error(error)

    def on_close(self, ws: WebSocket, close_status_code: str, close_msg: str) -> None:
        self._log.info("### WebSocket Closed ###")

    def on_open(self, ws: WebSocket) -> None:
        self._log.info("### WebSocket Opened ###")

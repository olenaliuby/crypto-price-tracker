from loguru import logger
from PyQt6.QtCore import QObject, pyqtSignal, pyqtSlot


class DataHandler(QObject):
    processed_price_update_signal = pyqtSignal(dict)

    def __init__(self) -> None:
        super().__init__()
        self._previous_prices = {}
        self._log = logger.bind(name="DataHandler")

    @staticmethod
    def determine_color(price: float, previous_price: float | None) -> str:
        """Determines the color based on price comparison."""
        if previous_price is None:
            return "white"
        if price > previous_price:
            return "green"
        if price < previous_price:
            return "red"
        return "white"

    def process_price_data(self, data: dict) -> dict:
        """Processes the received data and returns a dictionary with the processed data."""
        processed_data = {}
        try:
            trade_info = data.get("data")
            if not trade_info:
                self._log.warning("Received data is missing the 'data' field.")
                return processed_data

            coin = trade_info.get("s")
            price_str = trade_info.get("p")
            if not coin or not price_str:
                self._log.warning("Received data is missing the 'coin' or 'price'.")
                return processed_data

            try:
                price = float(price_str)
            except ValueError:
                self._log.error(f"Invalid price format: {price_str}")
                return processed_data

            previous_price = self._previous_prices.get(coin, {}).get("price")
            color = self.determine_color(price, previous_price)

            processed_data[coin] = {"price": price, "color": color}
            self._previous_prices[coin] = {"price": price}

        except Exception as e:
            self._log.error(f"An unexpected error occurred: {e}")
        return processed_data

    @pyqtSlot(dict)
    def handle_data(self, data: dict) -> None:
        """Handles the received data and emits a signal with the processed data."""
        try:
            processed_data = self.process_price_data(data)
            self.processed_price_update_signal.emit(processed_data)  # noqa
        except Exception as e:
            self._log.error(f"An error occurred while handling data: {e}")

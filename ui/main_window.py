from PyQt6.QtWidgets import QMainWindow, QVBoxLayout, QWidget

from utils.coins import CRYPTO_COINS
from .widgets.price_widget import PriceWidget


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Crypto Price Tracker")
        self.setGeometry(100, 100, 800, 600)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(10, 10, 10, 10)
        self.layout.setSpacing(10)
        self.central_widget.setLayout(self.layout)

        self.coins = CRYPTO_COINS

        self.price_widgets = {}
        for coin in self.coins.keys():
            price_widget = PriceWidget()
            self.layout.addWidget(price_widget)
            self.price_widgets[coin] = price_widget

    def update_price_widgets(self, data: dict) -> None:
        for coin, info in data.items():
            if coin in self.price_widgets:
                self.price_widgets[coin].update_price(
                    coin, info["price"], info["color"]
                )

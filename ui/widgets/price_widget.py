from PyQt6.QtWidgets import QVBoxLayout, QWidget, QLabel, QGridLayout
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt


class PriceWidget(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.layout = None
        self.grid_layout = None
        self.ticker_label = None
        self.price_label = None
        self.init_ui()

    def init_ui(self) -> None:
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(10, 10, 10, 10)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.setLayout(self.layout)

        self.grid_layout = QGridLayout()
        self.layout.addLayout(self.grid_layout)

        self.ticker_label = QLabel("BTC")
        self.ticker_label.setFont(QFont("Arial", 20))

        self.price_label = QLabel("$0.00")
        self.price_label.setFont(QFont("Arial", 20))

        self.grid_layout.addWidget(self.ticker_label, 0, 0)
        self.grid_layout.addWidget(self.price_label, 0, 1)

        self.ticker_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.price_label.setAlignment(Qt.AlignmentFlag.AlignLeft)

    def update_price(self, ticket: str, price: float, color: str) -> None:
        ticket_name = ticket.split("USDT")[0]
        self.ticker_label.setText(ticket_name)
        self.price_label.setText(f"${price}")

        self.price_label.setStyleSheet(f"color: {color};")

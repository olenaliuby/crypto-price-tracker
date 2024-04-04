from PyQt6.QtWidgets import QApplication
from websocket_client.client import WebSocketClient
from data_handler.handler import DataHandler
from ui.main_window import MainWindow


def main() -> None:
    app = QApplication([])
    websocket_client = WebSocketClient()
    data_handler = DataHandler()
    window = MainWindow()
    window.show()

    websocket_client.price_update.connect(data_handler.handle_data)
    data_handler.price_update_signal.connect(
        lambda data: window.update_price_widgets(data)
    )
    websocket_client.start()

    app.exec()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Exiting...")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

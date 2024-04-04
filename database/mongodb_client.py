from datetime import datetime

from PyQt6.QtCore import QObject, pyqtSlot
from motor.motor_asyncio import AsyncIOMotorClient
from loguru import logger

from settings import MONGODB_URI


class MongoDBClient(QObject):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.client = AsyncIOMotorClient(MONGODB_URI)
        self.db = self.client["crypto_prices"]
        self.collection = self.db["price_updates"]
        self._log = logger.bind(name="MongoDBClient")

    @pyqtSlot(dict)
    async def store_price_data(self, data: dict) -> None:
        for symbol, details in data.items():
            document = {
                "symbol": symbol.split("USDT")[0],
                "price": details["price"],
                "date": datetime.utcnow(),
            }
            try:
                await self.collection.insert_one(document)
            except Exception as e:
                self._log.error(f"Failed to store data in MongoDB for {symbol}: {e}")

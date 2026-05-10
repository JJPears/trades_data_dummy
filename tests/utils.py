from datetime import datetime
from src.common.enums import ProductType


class DummyTrade:
    def __init__(
        self,
        payload: dict | None = None,
        product_type: ProductType | None = None,
        trade_date: datetime | None = None,
    ):
        self.payload = payload or {}
        self.product_type = product_type
        self.trade_date = trade_date

    def model_dump(self):
        return self.payload

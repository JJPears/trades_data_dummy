from src.common.enums import ProductType
from src.models.trade_models import TradeCollection
from src.factories.trade_factory import TradeFactory

import random


class TradeService:
    def __init__(self, factory: TradeFactory):
        self.factory = factory

    # For large datasets we could have duplicate unique identifiers as these are randomly generated
    def create_trades(
        self,
        n: int = 15,
        product_types: list[ProductType] | None = None,
        sort: bool = True,
    ) -> TradeCollection:
        trades = TradeCollection()
        available_types = product_types or list(ProductType)
        # Potentially need error handling

        for _ in range(n):
            product_type = random.choice(available_types)
            trade = self.factory.create(product_type)
            trades.append(trade)

        if sort:
            trades.sort(key=lambda t: t.trade_date, reverse=True)

        return trades


if __name__ == "__main__":
    service = TradeService(TradeFactory())
    product_types = [ProductType.FX_OPTION]
    trades = service.create_trades(product_types=product_types)
    trades.to_csv("/home/josh/coding/trades_data_dummy/src/output.csv")

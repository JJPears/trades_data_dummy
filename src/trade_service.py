from src.common.enums import ProductType
from src.models.trade_collection import TradeCollection
from src.factories.trade_factory import (
    create_bullet_bond_trade,
    create_ir_swap_trade,
    create_fx_option_trade,
    create_fx_spot_trade,
)

import random


class TradeService:
    def __init__(self):
        self.FACTORY_MAP = {
            ProductType.BOND_FIXED: create_bullet_bond_trade,
            ProductType.IR_SWAP: create_ir_swap_trade,
            ProductType.FX_OPTION: create_fx_option_trade,
            ProductType.FX_SPOT: create_fx_spot_trade,
        }
        self.ALL_PRODUCT_TYPES = list(self.FACTORY_MAP.keys())

    # For large datasets we could have duplicate unique identifiers as these are randomly generated
    def create_trades(
        self,
        n: int = 15,
        product_types: list[ProductType] | None = None,
        sort: bool = True,
    ) -> TradeCollection:
        trades = TradeCollection()
        available_types = product_types or self.ALL_PRODUCT_TYPES
        # Potentially need error handling

        for _ in range(n):
            product_type = random.choice(available_types)
            trade = self.FACTORY_MAP[product_type]()
            trades.append(trade)

        if sort:
            trades.sort(key=lambda t: t.trade_date, reverse=True)

        return trades

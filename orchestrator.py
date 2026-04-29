from common.enums import ProductType
from models.asset_classes import Trade
from trade_factory import (
    create_bullet_bond_trade,
    create_ir_swap_trade,
    create_fx_option_trade,
    create_fx_spot_trade,
)

import random

FACTORY_MAP = {
    ProductType.BOND_FIXED: create_bullet_bond_trade,
    ProductType.IR_SWAP: create_ir_swap_trade,
    ProductType.FX_OPTION: create_fx_option_trade,
    ProductType.FX_SPOT: create_fx_spot_trade,
}


def generate_trades(n:int = 15, product_types: list[ProductType] | None = None) -> list[Trade]:
    trades = []

    for _ in range(n):
        if product_types:
            product_type = random.choice(product_types)
            # Add error handling if passed something we're not expecting ^^
        else:
            product_type = random.choice(list(ProductType))
        
        trade = FACTORY_MAP[product_type]()
        trades.append(trade)

    return trades
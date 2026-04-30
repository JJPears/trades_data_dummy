from common.enums import ProductType
from models.asset_classes import Trade
from factories.trade_factory import (
    create_bullet_bond_trade,
    create_ir_swap_trade,
    create_fx_option_trade,
    create_fx_spot_trade,
)

import random
import pandas as pd
from typing import Any

FACTORY_MAP = {
    ProductType.BOND_FIXED: create_bullet_bond_trade,
    ProductType.IR_SWAP: create_ir_swap_trade,
    ProductType.FX_OPTION: create_fx_option_trade,
    ProductType.FX_SPOT: create_fx_spot_trade,
}

ALL_PRODUCT_TYPES = list(FACTORY_MAP.keys())


# For large datasets we could have duplicate unique identifiers as these are randomly generated
def create_trades(
    n: int = 15,
    product_types: list[ProductType] | None = None,
    sort: bool = True,
) -> list[Trade]:

    trades = []
    available_types = product_types or ALL_PRODUCT_TYPES
    # Potentially need error handling

    for _ in range(n):
        product_type = random.choice(available_types)
        trade = FACTORY_MAP[product_type]()
        trades.append(trade)

    return (
        sorted(trades, key=lambda t: t.trade_date, reverse=True)
        if sort
        else trades
    )


def to_df(trades: list[Trade]) -> pd.DataFrame:
    rows = [t.model_dump() for t in trades]
    return pd.DataFrame(rows)


def to_csv(file_path: str, trades: list[Trade]) -> None:
    df = to_df(trades)
    df.to_csv(file_path, index=False)


def to_dicts(trades: list[Trade]) -> list[dict[str, Any]]:
    return [t.model_dump() for t in trades]

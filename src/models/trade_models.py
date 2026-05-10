from pydantic import BaseModel
from datetime import datetime
from typing import Any
import pandas as pd
from src.common.utils import validate_csv_file_path
from src.common.enums import (
    AssetClass,
    ProductType,
    CouponFrequency,
    DayCount,
    Direction,
    OptionType,
    PayReceive,
    Ccy,
)


class Trade(BaseModel):
    trade_id: str
    trade_date: datetime
    asset_class: AssetClass
    product_type: ProductType
    notional: float


# Rates
class BulletBondTrade(Trade):
    issuer: str
    coupon_rate: float
    coupon_freq: CouponFrequency
    issue_date: datetime
    maturity_date: datetime
    day_count: DayCount
    currency: Ccy
    # potentially add rating and credit spread


class IRSwapTrade(Trade):
    fixed_rate: float
    float_index: str
    start_date: datetime
    maturity_date: datetime
    fixed_leg_freq: CouponFrequency
    floating_leg_freq: CouponFrequency
    day_count_fixed: DayCount
    day_count_floating: DayCount
    currency: Ccy


# FX
class FXOptionTrade(Trade):
    underlying: str
    notional_ccy: Ccy
    direction: Direction
    option_type: OptionType
    strike: float
    expiry_date: datetime
    pay_receive_fixed: PayReceive


class FXTrade(Trade):
    ccy_pair: str
    direction: Direction
    value_date: datetime


class TradeCollection(list):
    def to_df(self) -> pd.DataFrame:
        rows = [t.model_dump() for t in self]
        return pd.DataFrame(rows)

    def to_dicts(self) -> list[dict[str, Any]]:
        return [t.model_dump() for t in self]

    def to_csv(self, file_path):

        validate_csv_file_path(file_path)

        df = self.to_df()
        df.to_csv(file_path, index=False)

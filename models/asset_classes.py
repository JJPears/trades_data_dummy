from pydantic import BaseModel
from datetime import datetime
from common.enums import (
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
    currency: Ccy


# Rates
class BulletBond(Trade):
    issuer: str
    coupon_rate: float
    coupon_freq: CouponFrequency
    issue_date: datetime
    maturity_date: datetime
    day_count: DayCount
    # potentially add rating and credit spread


class IRSwap(Trade):
    fixed_rate: float
    float_index: str
    start_date: datetime
    maturity_date: datetime
    fixed_leg_freq: CouponFrequency
    floating_leg_freq: CouponFrequency
    day_count_fixed: DayCount
    day_count_floating: DayCount


# FX
class FXOption(Trade):
    ccy_pair: str
    direction: Direction
    option_type: OptionType
    strike: float
    expiry_date: datetime
    domestic_ccy: Ccy
    foreign_ccy: Ccy
    pay_receive_fixe: PayReceive


class FXSpot(Trade):
    ccy_pair: str
    direction: Direction
    value_date: datetime

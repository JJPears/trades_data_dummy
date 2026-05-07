from datetime import datetime

from src.common.constants import FX_PAIRS, ISSUERS
from src.common.enums import (
    AssetClass,
    CouponFrequency,
    DayCount,
    Direction,
    OptionType,
    PayReceive,
    ProductType,
    Ccy,
)
from src.factories.trade_factory import (
    create_bullet_bond_trade,
    create_fx_option_trade,
    create_fx_spot_trade,
    create_ir_swap_trade,
)
from src.models.asset_classes import BulletBond, FXOption, FXSpot, IRSwap


def test_create_bullet_bond_trade_returns_bulletbond():
    trade = create_bullet_bond_trade()

    assert isinstance(trade, BulletBond)
    assert trade.asset_class == AssetClass.RATES
    assert trade.product_type == ProductType.BOND_FIXED
    assert len(trade.trade_id) == 12
    assert trade.issuer in ISSUERS
    assert isinstance(trade.coupon_freq, CouponFrequency)
    assert isinstance(trade.day_count, DayCount)
    assert trade.issue_date <= trade.maturity_date


def test_create_ir_swap_trade_returns_irswap():
    trade = create_ir_swap_trade()

    assert isinstance(trade, IRSwap)
    assert trade.asset_class == AssetClass.RATES
    assert trade.product_type == ProductType.IR_SWAP
    assert len(trade.trade_id) == 12
    assert isinstance(trade.fixed_leg_freq, CouponFrequency)
    assert isinstance(trade.floating_leg_freq, CouponFrequency)
    assert isinstance(trade.day_count_fixed, DayCount)
    assert isinstance(trade.day_count_floating, DayCount)
    assert trade.start_date <= trade.maturity_date
    assert trade.start_date <= trade.trade_date


def test_create_fx_option_trade_returns_fxoption():
    trade = create_fx_option_trade()

    assert isinstance(trade, FXOption)
    assert trade.asset_class == AssetClass.FX
    assert trade.product_type == ProductType.FX_OPTION
    assert len(trade.trade_id) == 12
    assert trade.direction in Direction
    assert trade.option_type in OptionType
    assert trade.underlying in FX_PAIRS
    assert trade.notional_ccy in Ccy
    assert trade.pay_receive_fixed in PayReceive
    assert trade.trade_date <= trade.expiry_date


def test_create_fx_spot_trade_returns_fxspot():
    trade = create_fx_spot_trade()

    assert isinstance(trade, FXSpot)
    assert trade.asset_class == AssetClass.FX
    assert trade.product_type == ProductType.FX_SPOT
    assert len(trade.trade_id) == 12
    assert trade.ccy_pair in FX_PAIRS
    assert trade.direction in Direction
    assert isinstance(trade.trade_date, datetime)
    assert isinstance(trade.value_date, datetime)

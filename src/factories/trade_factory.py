from src.models.trade_models import (
    BulletBondTrade,
    IRSwapTrade,
    FXOptionTrade,
    FXTrade,
)
from src.common.utils import (
    generate_trade_id,
    generate_date,
    generate_notional,
    generate_currency,
    generate_issuer,
    generate_coupon_frequency,
    generate_day_count,
    generate_rate,
    generate_float_index,
    generate_ccy_pair,
    generate_direction,
    generate_option_type,
    generate_strike,
    generate_pay_receive,
)
from src.common.enums import AssetClass, ProductType, Ccy


def create_bullet_bond_trade() -> BulletBondTrade:
    # This is not a realistic life cycle for our bond and there will be bias due to
    # maturity date being dependent on trade date

    issue_date = generate_date()
    trade_date = generate_date(start_date=issue_date)
    maturity_date = generate_date(start_date=trade_date)

    bond_data = {
        "trade_id": generate_trade_id(),
        "trade_date": trade_date,
        "asset_class": AssetClass.RATES,
        "product_type": ProductType.BOND_FIXED,
        "notional": generate_notional(),
        "currency": generate_currency(),
        "issuer": generate_issuer(),
        "coupon_rate": generate_rate(),
        "coupon_freq": generate_coupon_frequency(),
        "issue_date": issue_date,
        "maturity_date": maturity_date,
        "day_count": generate_day_count(),
    }

    return BulletBondTrade(**bond_data)


def create_ir_swap_trade() -> IRSwapTrade:

    start_date = generate_date()
    maturity_date = generate_date(start_date=start_date)

    swap_data = {
        "trade_id": generate_trade_id(),
        "trade_date": generate_date(start_date=start_date),
        "asset_class": AssetClass.RATES,
        "product_type": ProductType.IR_SWAP,
        "notional": generate_notional(),
        "currency": generate_currency(),
        "fixed_rate": generate_rate(),
        "float_index": generate_float_index(),
        "start_date": start_date,
        "maturity_date": maturity_date,
        "fixed_leg_freq": generate_coupon_frequency(),
        "floating_leg_freq": generate_coupon_frequency(),
        "day_count_fixed": generate_day_count(),
        "day_count_floating": generate_day_count(),
    }

    return IRSwapTrade(**swap_data)


def create_fx_option_trade() -> FXOptionTrade:
    trade_date = generate_date()
    expiry_date = generate_date(start_date=trade_date)

    underlying = generate_ccy_pair()
    notional_ccy = underlying.split("/")[-1]
    fx_option_data = {
        "trade_id": generate_trade_id(),
        "trade_date": trade_date,
        "asset_class": AssetClass.FX,
        "product_type": ProductType.FX_OPTION,
        "notional": generate_notional(),
        "direction": generate_direction(),
        "option_type": generate_option_type(),
        "strike": generate_strike(),
        "expiry_date": expiry_date,
        "underlying": underlying,
        "notional_ccy": Ccy[notional_ccy],
        "pay_receive_fixed": generate_pay_receive(),
    }

    return FXOptionTrade(**fx_option_data)


def create_fx_spot_trade() -> FXTrade:

    fx_spot_data = {
        "trade_id": generate_trade_id(),
        "trade_date": generate_date(),
        "asset_class": AssetClass.FX,
        "product_type": ProductType.FX_SPOT,
        "notional": generate_notional(),
        "ccy_pair": generate_ccy_pair(),
        "direction": generate_direction(),
        "value_date": generate_date(),
    }

    return FXTrade(**fx_spot_data)

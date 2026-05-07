from enum import StrEnum


class AssetClass(StrEnum):
    FX = "FX"
    RATES = "RATES"


class ProductType(StrEnum):
    # FX
    FX_SPOT = "FX_SPOT"
    FX_OPTION = "FX_OPTION"

    # Rates
    IR_SWAP = "IR_SWAP"
    BOND_FIXED = "BOND_FIXED"


class Direction(StrEnum):
    BUY = "BUY"
    SELL = "SELL"


class PayReceive(StrEnum):
    PAY = "PAY"
    RECEIVE = "RECEIVE"


class OptionType(StrEnum):
    CALL = "CALL"
    PUT = "PUT"


class DayCount(StrEnum):
    ACT_360 = "ACT/360"
    ACT_365 = "ACT/365"
    THIRTY_360 = "30/360"


class CouponFrequency(StrEnum):
    ANNUAL = "ANNUAL"
    SEMI_ANNUAL = "SEMI_ANNUAL"
    QUARTERLY = "QUARTERLY"
    MONTHLY = "MONTHLY"


class Ccy(StrEnum):
    GBP = "GBP"
    EUR = "EUR"
    USD = "USD"
    JPY = "JPY"

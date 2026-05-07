import os
import random
import string
from datetime import datetime, timedelta
from src.common.enums import (
    Ccy,
    CouponFrequency,
    DayCount,
    Direction,
    OptionType,
    PayReceive,
)
from src.common.constants import (
    ISSUERS,
    FLOAT_INDEXES,
    FX_PAIRS,
    NOTIONAL_MAX,
    NOTIONAL_MIN,
    RATE_MAX,
    RATE_MIN,
    STRIKE_MAX,
    STRIKE_MIN,
)


def generate_trade_id() -> str:
    return "".join(random.choices(string.ascii_uppercase + string.digits, k=12))


def generate_date(
    start_date: datetime = datetime(2020, 1, 1),
    end_date: datetime = datetime(2026, 12, 31),
) -> datetime:

    delta = (end_date - start_date).days
    return start_date + timedelta(days=random.randint(0, delta))


def generate_notional(
    min_val: float = NOTIONAL_MIN, max_val: float = NOTIONAL_MAX
) -> float:
    return random.uniform(min_val, max_val)


def generate_currency() -> Ccy:
    return random.choice(list(Ccy))


def generate_issuer() -> str:
    return random.choice(ISSUERS)


def generate_coupon_frequency() -> CouponFrequency:
    return random.choice(list(CouponFrequency))


def generate_day_count() -> DayCount:
    return random.choice(list(DayCount))


def generate_rate(
    min_val: float = RATE_MIN, max_val: float = RATE_MAX
) -> float:
    return random.uniform(min_val, max_val)


def generate_float_index() -> str:
    return random.choice(FLOAT_INDEXES)


def generate_ccy_pair() -> str:
    return random.choice(FX_PAIRS)


def generate_direction() -> Direction:
    return random.choice(list(Direction))


def generate_strike(
    min_val: float = STRIKE_MIN, max_val: float = STRIKE_MAX
) -> float:
    return random.uniform(min_val, max_val)


def generate_option_type() -> OptionType:
    return random.choice(list(OptionType))


def generate_pay_receive() -> PayReceive:
    return random.choice(list(PayReceive))


def validate_csv_file_path(file_path) -> None:
    if not isinstance(file_path, str):
        raise ValueError("file_path must be a string")

    if not file_path.lower().endswith(".csv"):
        raise ValueError("file_path must end with '.csv'")

    dir_path = os.path.dirname(file_path)
    if dir_path and not os.path.exists(dir_path):
        raise ValueError(f"Directory {dir_path} does not exist")
    if not os.access(dir_path or ".", os.W_OK):
        raise PermissionError(f"No write permission for directory {dir_path}")

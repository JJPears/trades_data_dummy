import random
import string
from datetime import datetime, timedelta
from common.enums import (
    Ccy,
    CouponFrequency,
    DayCount,
    Direction,
    OptionType,
    PayReceive,
)
from common.constants import (
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


def generate_trade_id():
    return "".join(random.choices(string.ascii_uppercase + string.digits, k=12))


def generate_date(
    start_date=datetime(2020, 1, 1), end_date=datetime(2026, 12, 31)
):

    delta = (end_date - start_date).days
    return start_date + timedelta(days=random.randint(0, delta))


def generate_notional(min_val=NOTIONAL_MIN, max_val=NOTIONAL_MAX):
    return random.uniform(min_val, max_val)


def generate_currency():
    return random.choice(list(Ccy))


def generate_issuer():
    return random.choice(ISSUERS)


def generate_coupon_frequency():
    return random.choice(list(CouponFrequency))


def generate_day_count():
    return random.choice(list(DayCount))


def generate_rate(min_val=RATE_MIN, max_val=RATE_MAX):
    return random.uniform(min_val, max_val)


def generate_float_index():
    return random.choice(FLOAT_INDEXES)


def generate_ccy_pair():
    return random.choice(FX_PAIRS)


def generate_direction():
    return random.choice(list(Direction))


def generate_strike(min_val=STRIKE_MIN, max_val=STRIKE_MAX):
    return random.uniform(min_val, max_val)


def generate_option_type():
    return random.choice(list(OptionType))


def generate_pay_receive():
    return random.choice(list(PayReceive))

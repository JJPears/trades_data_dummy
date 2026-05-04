import random
from datetime import datetime

from src.common.constants import FLOAT_INDEXES, FX_PAIRS, ISSUERS
from src.common.enums import (
    Ccy,
    CouponFrequency,
    DayCount,
    Direction,
    OptionType,
    PayReceive,
)
from src.common.utils import (
    generate_coupon_frequency,
    generate_ccy_pair,
    generate_currency,
    generate_date,
    generate_direction,
    generate_float_index,
    generate_issuer,
    generate_notional,
    generate_option_type,
    generate_pay_receive,
    generate_rate,
    generate_strike,
    generate_trade_id,
    generate_day_count,
)


def test_generate_trade_id_returns_12_characters():
    random.seed(0)
    trade_id = generate_trade_id()
    assert len(trade_id) == 12
    assert trade_id.isalnum()
    assert trade_id.upper() == trade_id


def test_generate_date_returns_date_within_range():
    start = datetime(2021, 1, 1)
    end = datetime(2021, 1, 10)
    date = generate_date(start_date=start, end_date=end)
    assert start <= date <= end


def test_generate_date_equal_start_end_returns_same_date():
    single = datetime(2022, 3, 15)
    assert generate_date(start_date=single, end_date=single) == single


def test_generate_notional_within_bounds():
    value = generate_notional(min_val=100.0, max_val=200.0)
    assert 100.0 <= value <= 200.0


def test_generate_rate_within_bounds():
    value = generate_rate(min_val=0.01, max_val=0.05)
    assert 0.01 <= value <= 0.05


def test_generate_strike_within_bounds():
    value = generate_strike(min_val=50, max_val=150)
    assert 50 <= value <= 150


def test_generate_currency_returns_enum():
    assert isinstance(generate_currency(), Ccy)


def test_generate_coupon_frequency_returns_enum():
    assert isinstance(generate_coupon_frequency(), CouponFrequency)


def test_generate_day_count_returns_enum():
    assert isinstance(generate_day_count(), DayCount)


def test_generate_direction_returns_enum():
    assert isinstance(generate_direction(), Direction)


def test_generate_option_type_returns_enum():
    assert isinstance(generate_option_type(), OptionType)


def test_generate_pay_receive_returns_enum():
    assert isinstance(generate_pay_receive(), PayReceive)


def test_generate_issuer_returns_known_value():
    assert generate_issuer() in ISSUERS


def test_generate_float_index_returns_known_value():
    assert generate_float_index() in FLOAT_INDEXES


def test_generate_ccy_pair_returns_known_value():
    assert generate_ccy_pair() in FX_PAIRS

import random
import math
import pytest
import os
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
    validate_csv_file_path,
    parse_tenor,
    linear_interpolate,
    bilinear_interpolate,
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


@pytest.mark.parametrize(
    "tenor, expected",
    [
        ("1D", 1 / 365),
        ("7D", 7 / 365),
        ("1W", 1 / 52),
        ("2W", 2 / 52),
        ("1M", 1 / 12),
        ("3M", 0.25),
        ("6M", 0.5),
        ("1Y", 1.0),
        ("2Y", 2.0),
        (" 3m ", 0.25),
    ],
)
def test_parse_tenor_valid(tenor, expected):
    result = parse_tenor(tenor)
    assert math.isclose(result, expected)


@pytest.mark.parametrize(
    "tenor",
    [
        "",
        "ABC",
        "1Q",
        "Y1",
        "TENOR",
    ],
)
def test_parse_tenor_invalid(tenor):
    with pytest.raises(ValueError):
        parse_tenor(tenor)


def test_linear_interpolate_exact_match():
    x_points = [1.0, 2.0, 3.0]
    y_points = [10.0, 20.0, 30.0]

    result = linear_interpolate(x_points, y_points, 2.0)

    assert result == 20.0


def test_linear_interpolate_midpoint():
    x_points = [1.0, 2.0]
    y_points = [10.0, 20.0]

    result = linear_interpolate(x_points, y_points, 1.5)

    assert result == 15.0


def test_linear_interpolate_left_boundary():
    x_points = [1.0, 2.0]
    y_points = [10.0, 20.0]

    result = linear_interpolate(x_points, y_points, 0.5)

    assert result == 10.0


def test_linear_interpolate_right_boundary():
    x_points = [1.0, 2.0]
    y_points = [10.0, 20.0]

    result = linear_interpolate(x_points, y_points, 3.0)

    assert result == 20.0


def test_linear_interpolate_non_uniform_spacing():
    x_points = [1.0, 3.0]
    y_points = [10.0, 30.0]

    result = linear_interpolate(x_points, y_points, 2.0)

    assert result == 20.0


def test_linear_interpolate_length_mismatch():
    with pytest.raises(ValueError):
        linear_interpolate([1.0], [1.0, 2.0], 1.0)


def test_linear_interpolate_not_enough_points():
    with pytest.raises(ValueError):
        linear_interpolate([1.0], [2.0], 1.0)


def test_bilinear_interpolate_center():
    x_points = [0.0, 1.0]
    y_points = [0.0, 1.0]

    z_grid = [
        [0.0, 10.0],
        [20.0, 30.0],
    ]

    result = bilinear_interpolate(
        x=0.5,
        y=0.5,
        x_points=x_points,
        y_points=y_points,
        z_grid=z_grid,
    )

    assert result == 15.0


def test_bilinear_interpolate_exact_corner():
    x_points = [0.0, 1.0]
    y_points = [0.0, 1.0]

    z_grid = [
        [1.0, 2.0],
        [3.0, 4.0],
    ]

    result = bilinear_interpolate(
        x=0.0,
        y=0.0,
        x_points=x_points,
        y_points=y_points,
        z_grid=z_grid,
    )

    assert result == 1.0


def test_bilinear_interpolate_exact_grid_point():
    x_points = [0.0, 1.0]
    y_points = [0.0, 1.0]

    z_grid = [
        [1.0, 2.0],
        [3.0, 4.0],
    ]

    result = bilinear_interpolate(
        x=1.0,
        y=1.0,
        x_points=x_points,
        y_points=y_points,
        z_grid=z_grid,
    )

    assert result == 4.0


def test_bilinear_interpolate_edge():
    x_points = [0.0, 1.0]
    y_points = [0.0, 1.0]

    z_grid = [
        [0.0, 10.0],
        [20.0, 30.0],
    ]

    result = bilinear_interpolate(
        x=0.5,
        y=0.0,
        x_points=x_points,
        y_points=y_points,
        z_grid=z_grid,
    )

    assert result == 10.0


def test_bilinear_interpolate_outside_grid_clamps():
    x_points = [0.0, 1.0]
    y_points = [0.0, 1.0]

    z_grid = [
        [0.0, 10.0],
        [20.0, 30.0],
    ]

    result = bilinear_interpolate(
        x=2.0,
        y=2.0,
        x_points=x_points,
        y_points=y_points,
        z_grid=z_grid,
    )

    assert result == 60.0


def test_validate_csv_file_path_valid(tmp_path):
    file_path = tmp_path / "output.csv"

    validate_csv_file_path(str(file_path))


def test_validate_csv_file_path_uppercase_extension(tmp_path):
    file_path = tmp_path / "output.CSV"

    validate_csv_file_path(str(file_path))


@pytest.mark.parametrize(
    "invalid_input",
    [
        None,
        123,
        12.5,
        [],
        {},
    ],
)
def test_validate_csv_file_path_non_string(invalid_input):
    with pytest.raises(ValueError, match="file_path must be a string"):
        validate_csv_file_path(invalid_input)


@pytest.mark.parametrize(
    "invalid_path",
    [
        "file.txt",
        "filecsv",
        "file.csv.backup",
        "",
    ],
)
def test_validate_csv_file_path_invalid_extension(invalid_path):
    with pytest.raises(ValueError, match="must end with '.csv'"):
        validate_csv_file_path(invalid_path)


def test_validate_csv_file_path_missing_directory(tmp_path):
    missing_dir = tmp_path / "does_not_exist"
    file_path = missing_dir / "output.csv"

    with pytest.raises(ValueError, match="does not exist"):
        validate_csv_file_path(str(file_path))


def test_validate_csv_file_path_no_write_permission(monkeypatch, tmp_path):
    file_path = tmp_path / "output.csv"

    monkeypatch.setattr(os, "access", lambda *args, **kwargs: False)

    with pytest.raises(PermissionError, match="No write permission"):
        validate_csv_file_path(str(file_path))


def test_validate_csv_file_path_current_directory(monkeypatch):
    monkeypatch.setattr(os, "access", lambda *args, **kwargs: True)

    # Should not raise
    validate_csv_file_path("output.csv")

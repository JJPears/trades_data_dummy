import os
import random
import string
from datetime import datetime, timedelta
from bisect import bisect_left
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


def generate_rate(min_val: float = RATE_MIN, max_val: float = RATE_MAX) -> float:
    return random.uniform(min_val, max_val)


def generate_float_index() -> str:
    return random.choice(FLOAT_INDEXES)


def generate_ccy_pair() -> str:
    return random.choice(FX_PAIRS)


def generate_direction() -> Direction:
    return random.choice(list(Direction))


def generate_strike(min_val: float = STRIKE_MIN, max_val: float = STRIKE_MAX) -> float:
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


def parse_tenor(tenor: str) -> float:
    """
    Convert tenor string to years.

    TODO This will need to be updated to handle daycounts as it's just an approximation currently.

    Examples:
        '1D' -> 1/365
        '1W' -> 1/52
        '1M' -> 1/12
        '3M' -> 0.25
        '1Y' -> 1.0
        '2Y' -> 2.0
    """
    tenor = tenor.upper().strip()

    if tenor.endswith("D"):
        return float(tenor[:-1]) / 365.0
    elif tenor.endswith("W"):
        return float(tenor[:-1]) / 52.0
    elif tenor.endswith("M"):
        return float(tenor[:-1]) / 12.0
    elif tenor.endswith("Y"):
        return float(tenor[:-1])
    else:
        raise ValueError(
            f"Unknown tenor format: {tenor}. Use format like '1D', '3M', '1Y'"
        )


def linear_interpolate(x_points: list[float], y_points: list[float], x: float):
    """Linear interpolation to return y value for a given x. If y value already in y_points return this value and don't interpolate."""
    if len(x_points) != len(y_points):
        raise ValueError("x_points and y_points must have same length")
    if len(x_points) < 2:
        raise ValueError("Need at least 2 points for interpolation")

    i = bisect_left(x_points, x)

    if i == 0:
        return y_points[0]
    if i == len(x_points):
        return y_points[-1]
    if i < len(x_points) and x_points[i] == x:
        return y_points[i]

    x1, x2 = x_points[i - 1], x_points[i]
    y1, y2 = y_points[i - 1], y_points[i]

    w = (x - x1) / (x2 - x1)
    return y1 + w * (y2 - y1)


def bilinear_interpolate(
    x: float,
    y: float,
    x_points: list[float],
    y_points: list[float],
    z_grid: list[list[float]],
) -> float:
    """
    Bilinear interpolation on a 2D grid.

    Args:
        x: First coordinate to interpolate at
        y: Second coordinate to interpolate at
        x_points: Known x coordinates (must be sorted ascending)
        y_points: Known y coordinates (must be sorted ascending)
        z_grid: 2D grid of z values: z_grid[x_idx][y_idx]

    Returns:
        Interpolated z value
    """

    i = bisect_left(x_points, x)
    j = bisect_left(y_points, y)

    if i == 0:
        i = 1
    if j == 0:
        j = 1
    if i == len(x_points):
        i = len(x_points) - 1
    if j == len(y_points):
        j = len(y_points) - 1

    x1, x2 = x_points[i - 1], x_points[i]
    y1, y2 = y_points[j - 1], y_points[j]

    q11 = z_grid[i - 1][j - 1]
    q21 = z_grid[i][j - 1]
    q12 = z_grid[i - 1][j]
    q22 = z_grid[i][j]

    wx = (x - x1) / (x2 - x1)
    wy = (y - y1) / (y2 - y1)

    return (
        (1 - wx) * (1 - wy) * q11
        + wx * (1 - wy) * q21
        + (1 - wx) * wy * q12
        + wx * wy * q22
    )

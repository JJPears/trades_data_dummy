from datetime import datetime

import pytest
from pydantic import ValidationError

from src.common.enums import Ccy
from src.models.market_data_models import (
    FXSpot,
    YieldCurve,
    FXVolSurface,
    MarketSnapshot,
)


def test_fxspot_valid():
    spot = FXSpot(
        valuation_date=datetime(2025, 1, 1),
        ccy_pair="EUR/USD",
        spot=1.10,
    )

    assert spot.spot == 1.10


@pytest.mark.parametrize("invalid_spot", [0, -1.0, -0.01])
def test_fxspot_invalid_spot(invalid_spot):
    with pytest.raises(ValidationError, match="Spot rate must be positive"):
        FXSpot(
            valuation_date=datetime(2025, 1, 1),
            ccy_pair="EUR/USD",
            spot=invalid_spot,
        )


@pytest.mark.parametrize("invalid_ccy_pair", ["USDEUR", "foo", "USD/BRZ"])
def test_fxspot_invalid_ccy_pair(invalid_ccy_pair):
    with pytest.raises(ValidationError, match="FX pair not supported"):
        FXSpot(
            valuation_date=datetime(2025, 1, 1),
            ccy_pair=invalid_ccy_pair,
            spot=1.10,
        )


def test_yield_curve_valid():
    curve = YieldCurve(
        valuation_date=datetime(2025, 1, 1),
        currency=Ccy.USD,
        tenors=["1Y", "2Y"],
        rates=[0.02, 0.03],
    )

    assert curve.rates == [0.02, 0.03]


def test_yield_curve_rejects_deeply_negative_rates():
    with pytest.raises(
        ValidationError, match="Rates cannot be deeply negative"
    ):
        YieldCurve(
            valuation_date=datetime(2025, 1, 1),
            currency=Ccy.USD,
            tenors=["1Y"],
            rates=[-0.10],
        )


def test_yield_curve_rejects_non_decimal_rates():
    with pytest.raises(
        ValidationError, match="Rates must be expressed as decimals"
    ):
        YieldCurve(
            valuation_date=datetime(2025, 1, 1),
            currency=Ccy.USD,
            tenors=["1Y"],
            rates=[5.0],
        )


def test_yield_curve_tenor_conversion():
    curve = YieldCurve(
        valuation_date=datetime(2025, 1, 1),
        currency=Ccy.USD,
        tenors=["6M", "1Y"],
        rates=[0.02, 0.03],
    )

    result = curve._tenor_years()

    assert result == [0.5, 1.0]


def test_yield_curve_get_rate_interpolated():
    curve = YieldCurve(
        valuation_date=datetime(2025, 1, 1),
        currency=Ccy.USD,
        tenors=["1Y", "2Y"],
        rates=[0.02, 0.04],
    )

    result = curve.get_rate(1.5)

    assert result == 0.03


def test_yield_curve_get_rate_exact_match():
    curve = YieldCurve(
        valuation_date=datetime(2025, 1, 1),
        currency=Ccy.USD,
        tenors=["1Y", "2Y"],
        rates=[0.02, 0.04],
    )

    result = curve.get_rate(2.0)

    assert result == 0.04


def test_fx_vol_surface_valid():
    surface = FXVolSurface(
        valuation_date=datetime(2025, 1, 1),
        ccy_pair="EUR/USD",
        tenors=["1Y", "2Y"],
        strikes=[1.0, 1.1],
        vols=[
            [0.10, 0.11],
            [0.12, 0.13],
        ],
    )

    assert surface.vols[0][0] == 0.10


def test_fx_vol_surface_rejects_non_positive_vols():
    with pytest.raises(ValidationError, match="Volatilities must be positive"):
        FXVolSurface(
            valuation_date=datetime(2025, 1, 1),
            ccy_pair="EUR/USD",
            tenors=["1Y"],
            strikes=[1.0],
            vols=[[0.0]],
        )


def test_fx_vol_surface_rejects_wrong_row_count():
    with pytest.raises(
        ValidationError, match="Vol grid has 1 rows but 2 tenors"
    ):
        FXVolSurface(
            valuation_date=datetime(2025, 1, 1),
            ccy_pair="EUR/USD",
            tenors=["1Y", "2Y"],
            strikes=[1.0],
            vols=[[0.10]],
        )


def test_fx_vol_surface_rejects_wrong_col_count():
    with pytest.raises(
        ValidationError,
        match="Vol grid row 0 has 1 cols but 2 strikes",
    ):
        FXVolSurface(
            valuation_date=datetime(2025, 1, 1),
            ccy_pair="EUR/USD",
            tenors=["1Y"],
            strikes=[1.0, 1.1],
            vols=[[0.10]],
        )


def test_fx_vol_surface_tenor_conversion():
    surface = FXVolSurface(
        valuation_date=datetime(2025, 1, 1),
        ccy_pair="EUR/USD",
        tenors=["6M", "1Y"],
        strikes=[1.0],
        vols=[
            [0.10],
            [0.11],
        ],
    )

    result = surface._tenor_years()

    assert result == [0.5, 1.0]


def test_fx_vol_surface_get_vol_interpolated():
    surface = FXVolSurface(
        valuation_date=datetime(2025, 1, 1),
        ccy_pair="EUR/USD",
        tenors=["1Y", "2Y"],
        strikes=[1.0, 2.0],
        vols=[
            [0.10, 0.20],
            [0.30, 0.40],
        ],
    )

    result = surface.get_vol(
        tenor_year=1.5,
        strike=1.5,
    )

    assert result == 0.25


@pytest.fixture
def market_snapshot():
    valuation_date = datetime(2025, 1, 1)

    return MarketSnapshot(
        valuation_date=valuation_date,
        fx_spots=[
            FXSpot(
                valuation_date=valuation_date,
                ccy_pair="EUR/USD",
                spot=1.10,
            )
        ],
        yield_curves=[
            YieldCurve(
                valuation_date=valuation_date,
                currency=Ccy.USD,
                tenors=["1Y", "2Y"],
                rates=[0.02, 0.04],
            )
        ],
        fx_vol_surfaces=[
            FXVolSurface(
                valuation_date=valuation_date,
                ccy_pair="EUR/USD",
                tenors=["1Y", "2Y"],
                strikes=[1.0, 2.0],
                vols=[
                    [0.10, 0.20],
                    [0.30, 0.40],
                ],
            )
        ],
    )


def test_market_snapshot_get_spot(market_snapshot):
    assert market_snapshot.get_spot("EUR/USD") == 1.10


def test_market_snapshot_get_spot_missing(market_snapshot):
    with pytest.raises(ValueError, match="No spot rate for GBP/USD"):
        market_snapshot.get_spot("GBP/USD")


def test_market_snapshot_get_yield_curve(market_snapshot):
    curve = market_snapshot.get_yield_curve(Ccy.USD)

    assert curve.currency == Ccy.USD


def test_market_snapshot_get_yield_curve_missing(market_snapshot):
    with pytest.raises(ValueError):
        market_snapshot.get_yield_curve(Ccy.EUR)


def test_market_snapshot_get_rate(market_snapshot):
    result = market_snapshot.get_rate(
        ccy=Ccy.USD,
        tenor_years=1.5,
    )

    assert result == 0.03


def test_market_snapshot_get_vol_surface(market_snapshot):
    surface = market_snapshot.get_vol_surface("EUR/USD")

    assert surface.ccy_pair == "EUR/USD"


def test_market_snapshot_get_vol_surface_missing(market_snapshot):
    with pytest.raises(
        ValueError,
        match="No vol surface found for GBP/USD",
    ):
        market_snapshot.get_vol_surface("GBP/USD")


def test_market_snapshot_get_vol(market_snapshot):
    result = market_snapshot.get_vol(
        ccy_pair="EUR/USD",
        tenor_years=1.5,
        strike=1.5,
    )

    assert result == 0.25

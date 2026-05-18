import pytest
from datetime import datetime, timezone

from src.factories.market_data_factory import (
    MarketDataFactory,
    generate_base_market_snapshot,
)


@pytest.fixture
def valuation_date():
    return datetime(2025, 1, 1, tzinfo=timezone.utc)


@pytest.fixture
def base_snapshot(valuation_date):
    return generate_base_market_snapshot(valuation_date)


def test_factory_determinism(base_snapshot, valuation_date):
    factory1 = MarketDataFactory(base_snapshot, valuation_date, seed=42)
    factory2 = MarketDataFactory(base_snapshot, valuation_date, seed=42)

    snap1 = factory1.generate()
    snap2 = factory2.generate()

    # FX spot
    assert snap1.fx_spots[0].spot == pytest.approx(snap2.fx_spots[0].spot)

    # Yield curves
    assert snap1.yield_curves[0].rates == pytest.approx(snap2.yield_curves[0].rates)

    # Vol surface
    flat1 = [v for row in snap1.fx_vol_surfaces[0].vols for v in row]
    flat2 = [v for row in snap2.fx_vol_surfaces[0].vols for v in row]

    assert flat1 == pytest.approx(flat2)


def test_valuation_date_propagation(base_snapshot, valuation_date):
    factory = MarketDataFactory(base_snapshot, valuation_date, seed=1)
    snapshot = factory.generate()

    assert snapshot.valuation_date == valuation_date

    for spot in snapshot.fx_spots:
        assert spot.valuation_date == valuation_date

    for curve in snapshot.yield_curves:
        assert curve.valuation_date == valuation_date

    for surface in snapshot.fx_vol_surfaces:
        assert surface.valuation_date == valuation_date


def test_fx_spot_structure_preserved(base_snapshot, valuation_date):
    factory = MarketDataFactory(base_snapshot, valuation_date, seed=123)
    snapshot = factory.generate()

    assert len(snapshot.fx_spots) == len(base_snapshot.fx_spots)
    assert snapshot.fx_spots[0].ccy_pair == base_snapshot.fx_spots[0].ccy_pair
    assert snapshot.fx_spots[0].spot != base_snapshot.fx_spots[0].spot


def test_yield_curve_structure_preserved(base_snapshot, valuation_date):
    factory = MarketDataFactory(base_snapshot, valuation_date, seed=123)
    snapshot = factory.generate()

    curve = snapshot.yield_curves[0]

    assert len(curve.rates) == len(base_snapshot.yield_curves[0].rates)
    assert curve.currency == base_snapshot.yield_curves[0].currency

    # rates should be different but same length
    assert curve.rates != base_snapshot.yield_curves[0].rates


def test_vol_surface_structure_preserved(base_snapshot, valuation_date):
    factory = MarketDataFactory(base_snapshot, valuation_date, seed=123)
    snapshot = factory.generate()

    surface = snapshot.fx_vol_surfaces[0]

    assert len(surface.vols) == len(base_snapshot.fx_vol_surfaces[0].vols)
    assert len(surface.vols[0]) == len(base_snapshot.fx_vol_surfaces[0].vols[0])

    # vols should have changed
    assert surface.vols != base_snapshot.fx_vol_surfaces[0].vols


def test_vol_floor_prevents_negative_vols(base_snapshot, valuation_date):
    factory = MarketDataFactory(base_snapshot, valuation_date, seed=999)
    snapshot = factory.generate(vol_noise=10.0)  # extreme noise

    for row in snapshot.fx_vol_surfaces[0].vols:
        for vol in row:
            assert vol >= 0.0001


def test_repeated_generation_does_not_mutate_base(base_snapshot, valuation_date):
    factory = MarketDataFactory(base_snapshot, valuation_date, seed=1)

    _ = factory.generate()
    _ = factory.generate()

    # base snapshot should remain unchanged
    assert base_snapshot.fx_spots[0].spot == 1.10
    assert base_snapshot.yield_curves[0].rates[0] == 0.045
    assert base_snapshot.fx_vol_surfaces[0].vols[0][0] == 0.11


def test_spot_moves_are_reasonable_bounds(base_snapshot, valuation_date):
    factory = MarketDataFactory(base_snapshot, valuation_date, seed=42)
    snapshot = factory.generate(spot_noise=0.01)

    spot = snapshot.fx_spots[0].spot

    # very loose sanity bounds (avoid brittle tests)
    assert 0.5 < spot < 2.0

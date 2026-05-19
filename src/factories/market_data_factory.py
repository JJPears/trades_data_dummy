import random
from datetime import datetime
from copy import deepcopy

from src.models.market_data_models import (
    MarketSnapshot,
    FXSpot,
    YieldCurve,
    FXVolSurface,
)
from src.common.enums import Ccy


class MarketDataFactory:
    def __init__(
        self,
        base_snapshot: MarketSnapshot,
        valuation_date: datetime,
        seed: int | None = None,
    ):
        self.base_snapshot = base_snapshot
        self.random = random.Random(seed)
        self.valuation_date = valuation_date

    def generate(
        self,
        spot_noise: float = 0.01,
        rate_noise: float = 0.001,
        vol_noise: float = 0.02,
    ) -> MarketSnapshot:
        """
        Generate a perturbed market snapshot.

        Parameters
        ----------
        spot_noise
            Relative FX spot perturbation magnitude.
            Example: 0.01 = ±1%

        rate_noise
            Absolute rate perturbation magnitude.
            Example: 0.001 = ±10bps

        vol_noise
            Relative vol perturbation magnitude.
            Example: 0.02 = ±2%
        """
        global_shock = self.random.gauss(0.0, 1.0)

        snapshot = deepcopy(self.base_snapshot)
        snapshot.valuation_date = self.valuation_date

        # These all modify underlying snapshot object
        self._shock_fx_spot(spot_noise, snapshot, global_shock)
        self._shock_yield_curve(rate_noise, snapshot, global_shock)
        self._shock_vol_surface(vol_noise, snapshot, global_shock)

        return snapshot

    def _shock_fx_spot(
        self, spot_noise: float, snapshot: MarketSnapshot, global_shock: float
    ) -> None:
        """
        Shocking fx spot by shocking each currency for currency pairs and also global shock

        TODO currently all ccys are shocked with the same global shock, implied beta of 1, could have beta generated for each ccy
        """
        global_shock = self.random.gauss(0.0, spot_noise)

        ccy_shock = {}
        for ccy in Ccy:
            ccy_shock[ccy] = self.random.gauss(0.0, spot_noise)

        for spot in snapshot.fx_spots:
            spot.valuation_date = self.valuation_date
            base_ccy, quote_ccy = spot.ccy_pair.split("/")

            move = ccy_shock[Ccy(base_ccy)] - ccy_shock[Ccy(quote_ccy)] + global_shock

            # TODO fix so this can't go negative
            spot.spot *= 1.0 + move

    def _shock_yield_curve(
        self, rate_noise: float, snapshot: MarketSnapshot, global_shock: float
    ) -> None:
        """
        Shocking yield curve with parallel move as well as slope gradient and global shock.

        Scaling global_shock with a beta of 0.0005
        """
        for curve in snapshot.yield_curves:
            curve.valuation_date = self.valuation_date
            shifted_rates = []

            level_shift = self.random.gauss(0.0, rate_noise)
            slope_shift = self.random.gauss(0.0, rate_noise * 0.5)

            # TODO expand to properly weight with tenors rather than index
            # Currently we weight based on index but [0, 1, 2, 3] is not comparable to [1M, 3M, 6M, 30Y]
            for i, rate in enumerate(curve.rates):
                # normalising value between 0 and 1 for weights
                tenor_weight = i / max(len(curve.rates) - 1, 1)

                adjusted_rate = (
                    rate
                    + level_shift
                    + slope_shift * tenor_weight
                    + 0.0005 * global_shock
                )

                shifted_rates.append(adjusted_rate)

            curve.rates = shifted_rates

    def _shock_vol_surface(
        self, vol_noise: float, snapshot: MarketSnapshot, global_shock: float
    ) -> None:
        """
        Shock all of our vols, scaled with beta of 0.01 for global shock
        regime (level) shift will move everything based on vol_noise
        individual vols will also be shifted by vol_noise scaled at 0.25
        """
        for surface in snapshot.fx_vol_surfaces:
            surface.valuation_date = self.valuation_date

            adjusted_grid = []
            vol_regime_shift = self.random.gauss(0.0, vol_noise)

            for row in surface.vols:
                adjusted_row = []
                for vol in row:
                    idiosyncratic_noise = self.random.gauss(
                        0.0,
                        vol_noise * 0.25,
                    )
                    total_move = (
                        vol_regime_shift + idiosyncratic_noise + 0.01 * global_shock
                    )

                    adjusted_vol = vol * (1.0 + total_move)
                    # floor to prevent negative or zero vol
                    adjusted_row.append(max(0.0001, adjusted_vol))

                adjusted_grid.append(adjusted_row)

            surface.vols = adjusted_grid


def generate_base_market_snapshot(valuation_date: datetime) -> MarketSnapshot:
    return MarketSnapshot(
        valuation_date=valuation_date,
        fx_spots=[
            FXSpot(valuation_date=valuation_date, ccy_pair="EUR/USD", spot=1.08),
            FXSpot(valuation_date=valuation_date, ccy_pair="GBP/USD", spot=1.27),
            FXSpot(valuation_date=valuation_date, ccy_pair="USD/JPY", spot=149.50),
            FXSpot(valuation_date=valuation_date, ccy_pair="EUR/GBP", spot=0.85),
        ],
        yield_curves=[
            YieldCurve(
                valuation_date=valuation_date,
                currency=Ccy.USD,
                tenors=["1M", "3M", "6M", "1Y", "2Y", "5Y", "10Y", "30Y"],
                rates=[0.053, 0.054, 0.054, 0.052, 0.049, 0.047, 0.046, 0.045],
            ),
            YieldCurve(
                valuation_date=valuation_date,
                currency=Ccy.EUR,
                tenors=["1M", "3M", "6M", "1Y", "2Y", "5Y", "10Y", "30Y"],
                rates=[0.039, 0.039, 0.038, 0.037, 0.034, 0.032, 0.031, 0.030],
            ),
            YieldCurve(
                valuation_date=valuation_date,
                currency=Ccy.GBP,
                tenors=["1M", "3M", "6M", "1Y", "2Y", "5Y", "10Y", "30Y"],
                rates=[0.052, 0.052, 0.051, 0.050, 0.047, 0.044, 0.043, 0.045],
            ),
            YieldCurve(
                valuation_date=valuation_date,
                currency=Ccy.JPY,
                tenors=["1M", "3M", "6M", "1Y", "2Y", "5Y", "10Y", "30Y"],
                rates=[0.001, 0.001, 0.002, 0.003, 0.004, 0.006, 0.010, 0.015],
            ),
        ],
        fx_vol_surfaces=[
            FXVolSurface(
                valuation_date=valuation_date,
                ccy_pair="EUR/USD",
                tenors=["1M", "3M", "6M", "1Y"],
                strikes=[0.95, 1.00, 1.05],
                vols=[
                    [0.075, 0.068, 0.074],
                    [0.073, 0.066, 0.072],
                    [0.071, 0.064, 0.070],
                    [0.069, 0.062, 0.068],
                ],
            ),
            FXVolSurface(
                valuation_date=valuation_date,
                ccy_pair="GBP/USD",
                tenors=["1M", "3M", "6M", "1Y"],
                strikes=[1.15, 1.20, 1.25],
                vols=[
                    [0.085, 0.078, 0.084],
                    [0.083, 0.076, 0.082],
                    [0.081, 0.074, 0.080],
                    [0.079, 0.072, 0.078],
                ],
            ),
            FXVolSurface(
                valuation_date=valuation_date,
                ccy_pair="USD/JPY",
                tenors=["1M", "3M", "6M", "1Y"],
                strikes=[145.0, 150.0, 155.0],
                vols=[
                    [0.095, 0.088, 0.092],
                    [0.092, 0.085, 0.089],
                    [0.089, 0.082, 0.086],
                    [0.086, 0.079, 0.083],
                ],
            ),
            FXVolSurface(
                valuation_date=valuation_date,
                ccy_pair="EUR/GBP",
                tenors=["1M", "3M", "6M", "1Y"],
                strikes=[0.82, 0.85, 0.88],
                vols=[
                    [0.065, 0.058, 0.064],
                    [0.063, 0.056, 0.062],
                    [0.061, 0.054, 0.060],
                    [0.059, 0.052, 0.058],
                ],
            ),
        ],
    )

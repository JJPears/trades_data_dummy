from pydantic import BaseModel, field_validator
from datetime import datetime
from src.common.enums import Ccy
from src.common.utils import (
    parse_tenor,
    linear_interpolate,
    bilinear_interpolate,
)


class FXSpot(BaseModel):
    valuation_date: datetime
    pair: str
    spot: float

    @field_validator("spot")
    @classmethod
    def validate_spot(cls, v: float) -> float:
        if v <= 0:
            raise ValueError("Spot rate must be positive")
        return v


class YieldCurve(BaseModel):
    """
    Yield curve for a single currency.

    Zero coupon rates for different tenors (tenors in the format of "1M", "3M", "1Y"...)
    Rates are in decimal form.
    """

    valuation_date: datetime
    currency: Ccy

    tenors: list[str]
    rates: list[float]

    @field_validator("rates")
    @classmethod
    def validate_rates(cls, v: list[float]) -> list[float]:
        if any(r < -0.05 for r in v):
            raise ValueError("Rates cannot be deeply negative")
        if any(r > 1.0 for r in v):
            raise ValueError("Rates must be expressed as decimals")
        return v

    def _tenor_years(self) -> list[float]:
        """Convert tenor strings to years for interpolation."""
        return [parse_tenor(t) for t in self.tenors]

    def get_rate(self, tenor_year: float) -> float:
        """For a given tenor in years return the"""
        tenor_years_list = self._tenor_years()
        return linear_interpolate(tenor_years_list, self.rates, tenor_year)


class FXVolSurface(BaseModel):
    """
    FX volatility surface for a currency pair.

    2D surface: tenors (time to expiry) X strikes (moneyness).
    """

    valuation_date: datetime
    pair: str

    tenors: list[str]
    strikes: list[float]
    vols: list[list[float]]

    @field_validator("vols")
    @classmethod
    def validate_vols(cls, v: list[list[float]], info) -> list[list[float]]:
        for row in v:
            if any(vol <= 0 for vol in row):
                raise ValueError("Volatilities must be positive")

        if "tenors" in info.data and "strikes" in info.data:
            expected_rows = len(info.data["tenors"])
            expected_cols = len(info.data["strikes"])

            if len(v) != expected_rows:
                raise ValueError(
                    f"Vol grid has {len(v)} rows but {expected_rows} tenors"
                )

            for i, row in enumerate(v):
                if len(row) != expected_cols:
                    raise ValueError(
                        f"Vol grid row {i} has {len(row)} cols but {expected_cols} strikes"
                    )

        return v

    def _tenor_years(self) -> list[float]:
        """Convert tenor strings to years for interpolation."""
        return [parse_tenor(t) for t in self.tenors]

    def get_vol(self, tenor_year: float, strike: float) -> float:
        tenor_years_list = self._tenor_years()
        return bilinear_interpolate(
            x=tenor_year,
            y=strike,
            x_points=tenor_years_list,
            y_points=self.strikes,
            z_grid=self.vols,
        )


class MarketSnapshot(BaseModel):
    """
    Complete market data snapshot at a single valuation date.

    Contains all market observables needed for pricing:
    - FX spot rates
    - Yield curves (zero rates)
    - FX volatility surfaces
    """

    valuation_date: datetime

    fx_spots: list[FXSpot]
    yield_curves: list[YieldCurve]
    fx_vol_surfaces: list[FXVolSurface]

    def get_spot(self, pair: str) -> float:
        """Get FX spot rate for a currency pair."""
        spot = next((s for s in self.fx_spots if s.pair == pair), None)
        if not spot:
            raise ValueError(f"No spot rate for {pair}")
        return spot.spot

    def get_yield_curve(self, ccy: Ccy) -> YieldCurve:
        """Get yield curve for a currency."""
        curve = next((c for c in self.yield_curves if c.currency == ccy), None)
        if not curve:
            raise ValueError(f"No yield curve for {ccy}")
        return curve

    def get_rate(self, ccy: Ccy, tenor_years: float) -> float:
        """Get interpolated zero rate for a currency and tenor."""
        curve = self.get_yield_curve(ccy)
        return curve.get_rate(tenor_years)

    def get_vol_surface(self, pair: str) -> FXVolSurface:
        """Get volatility surface for a currency pair."""
        surface = next(
            (v for v in self.fx_vol_surfaces if v.pair == pair), None
        )
        if surface is None:
            raise ValueError(f"No vol surface found for {pair}")
        return surface

    def get_vol(self, pair: str, tenor_years: float, strike: float) -> float:
        """Get interpolated volatility for a currency pair, tenor, and strike."""
        surface = self.get_vol_surface(pair)
        return surface.get_vol(tenor_years, strike)

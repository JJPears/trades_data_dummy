from datetime import datetime, timedelta
import random

from src.common.enums import ProductType
from src.models.trade_models import TradeCollection
from src.trade_service import TradeService
from tests.utils import DummyTrade


def test_create_trades_returns_sorted_trade_collection(monkeypatch):
    service = TradeService()

    base_date = datetime(2024, 1, 1)
    trade_dates = [
        base_date,
        base_date + timedelta(days=2),
        base_date + timedelta(days=1),
    ]
    service.FACTORY_MAP = {
        ProductType.BOND_FIXED: lambda: DummyTrade(
            product_type=ProductType.BOND_FIXED,
            trade_date=trade_dates[0],
        ),
        ProductType.IR_SWAP: lambda: DummyTrade(
            product_type=ProductType.IR_SWAP,
            trade_date=trade_dates[1],
        ),
        ProductType.FX_OPTION: lambda: DummyTrade(
            product_type=ProductType.FX_OPTION,
            trade_date=trade_dates[2],
        ),
    }
    selected_types = [
        ProductType.BOND_FIXED,
        ProductType.IR_SWAP,
        ProductType.FX_OPTION,
    ]

    sequence = iter(selected_types)
    monkeypatch.setattr(random, "choice", lambda _: next(sequence))

    trades = service.create_trades(n=3, product_types=selected_types)

    assert isinstance(trades, TradeCollection)
    assert [t.trade_date for t in trades] == sorted(
        [t.trade_date for t in trades], reverse=True
    )


def test_create_trades_respects_product_types_argument(monkeypatch):
    service = TradeService()

    base_date = datetime(2024, 1, 1)

    service.FACTORY_MAP = {
        ProductType.FX_SPOT: lambda: DummyTrade(
            product_type=ProductType.FX_SPOT,
            trade_date=base_date,
        ),
    }

    base_date = datetime(2024, 1, 1)

    monkeypatch.setattr(random, "choice", lambda _: ProductType.FX_SPOT)

    trades = service.create_trades(
        n=2,
        product_types=[ProductType.FX_SPOT],
        sort=False,
    )

    assert len(trades) == 2
    assert all(t.product_type == ProductType.FX_SPOT for t in trades)


def test_create_trades_with_sort_false_preserves_creation_order(monkeypatch):
    service = TradeService()

    base_date = datetime(2024, 1, 1)
    trade_dates = [
        base_date,
        base_date + timedelta(days=1),
        base_date + timedelta(days=2),
    ]
    service.FACTORY_MAP = {
        ProductType.FX_OPTION: lambda: DummyTrade(
            product_type=ProductType.FX_OPTION,
            trade_date=trade_dates[0],
        ),
        ProductType.FX_SPOT: lambda: DummyTrade(
            product_type=ProductType.FX_SPOT,
            trade_date=trade_dates[1],
        ),
        ProductType.IR_SWAP: lambda: DummyTrade(
            product_type=ProductType.IR_SWAP,
            trade_date=trade_dates[2],
        ),
    }
    selected_types = [
        ProductType.FX_OPTION,
        ProductType.FX_SPOT,
        ProductType.IR_SWAP,
    ]

    sequence = iter(selected_types)
    monkeypatch.setattr(random, "choice", lambda _: next(sequence))

    trades = service.create_trades(
        n=3,
        product_types=selected_types,
        sort=False,
    )

    assert [t.product_type for t in trades] == selected_types
    assert [t.trade_date for t in trades] == trade_dates

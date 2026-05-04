from datetime import datetime, timedelta

from src.common.enums import ProductType
from src.models.trade_collection import TradeCollection
from src import trade_service
from tests.utils import DummyTrade

def test_create_trades_returns_sorted_trade_collection(monkeypatch):
    base_date = datetime(2024, 1, 1)
    trade_dates = [
        base_date,
        base_date + timedelta(days=2),
        base_date + timedelta(days=1),
    ]
    selected_types = [
        ProductType.BOND_FIXED,
        ProductType.IR_SWAP,
        ProductType.FX_OPTION,
    ]

    factory_map = {
        product_type: (lambda pt=product_type, td=trade_dates[i]: DummyTrade(product_type=pt, trade_date=td))
        for i, product_type in enumerate(selected_types)
    }
    monkeypatch.setattr(trade_service, "FACTORY_MAP", factory_map)

    sequence = iter(selected_types)
    monkeypatch.setattr(trade_service.random, "choice", lambda options: next(sequence))

    trades = trade_service.create_trades(n=3)

    assert isinstance(trades, TradeCollection)
    assert [trade.trade_date for trade in trades] == sorted(
        [trade.trade_date for trade in trades], reverse=True
    )


def test_create_trades_respects_product_types_argument(monkeypatch):
    base_date = datetime(2024, 1, 1)
    monkeypatch.setattr(
        trade_service,
        "FACTORY_MAP",
        {
            ProductType.FX_SPOT: lambda: DummyTrade(product_type=ProductType.FX_SPOT, trade_date=base_date)
        },
    )
    monkeypatch.setattr(trade_service.random, "choice", lambda options: ProductType.FX_SPOT)

    trades = trade_service.create_trades(
        n=2, product_types=[ProductType.FX_SPOT], sort=False
    )

    assert len(trades) == 2
    assert all(trade.product_type == ProductType.FX_SPOT for trade in trades)


def test_create_trades_with_sort_false_preserves_creation_order(monkeypatch):
    base_date = datetime(2024, 1, 1)
    trade_dates = [
        base_date,
        base_date + timedelta(days=1),
        base_date + timedelta(days=2),
    ]
    selected_types = [
        ProductType.FX_OPTION,
        ProductType.FX_SPOT,
        ProductType.IR_SWAP,
    ]

    factory_map = {
        product_type: (lambda pt=product_type, td=trade_dates[i]: DummyTrade(product_type=pt, trade_date=td))
        for i, product_type in enumerate(selected_types)
    }
    monkeypatch.setattr(trade_service, "FACTORY_MAP", factory_map)

    sequence = iter(selected_types)
    monkeypatch.setattr(trade_service.random, "choice", lambda options: next(sequence))

    trades = trade_service.create_trades(n=3, sort=False)

    assert [trade.product_type for trade in trades] == selected_types
    assert [trade.trade_date for trade in trades] == trade_dates

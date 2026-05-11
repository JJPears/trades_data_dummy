from datetime import datetime, timedelta
import random

from src.common.enums import ProductType
from src.models.trade_models import TradeCollection
from src.trade_service import TradeService
from src.factories.trade_factory import TradeFactory
from tests.utils import DummyTrade




def test_create_trades_returns_sorted_trade_collection(monkeypatch):
    factory = TradeFactory()
    service = TradeService(factory)

    base_date = datetime(2024, 1, 1)
    trade_dates = [
        base_date,
        base_date + timedelta(days=2),
        base_date + timedelta(days=1),
    ]

    mapping = {
        ProductType.BOND_FIXED: DummyTrade(
            product_type=ProductType.BOND_FIXED,
            trade_date=trade_dates[0],
        ),
        ProductType.IR_SWAP: DummyTrade(
            product_type=ProductType.IR_SWAP,
            trade_date=trade_dates[1],
        ),
        ProductType.FX_OPTION: DummyTrade(
            product_type=ProductType.FX_OPTION,
            trade_date=trade_dates[2],
        ),
    }

    sequence = iter(mapping.keys())
    monkeypatch.setattr(random, "choice", lambda _: next(sequence))

    monkeypatch.setattr(factory, "create", lambda pt: mapping[pt])

    selected_types = list(mapping.keys())

    trades = service.create_trades(n=3, product_types=selected_types)

    assert isinstance(trades, TradeCollection)
    assert [t.trade_date for t in trades] == sorted(
        [t.trade_date for t in trades], reverse=True
    )


def test_create_trades_respects_product_types_argument(monkeypatch):
    factory = TradeFactory()
    service = TradeService(factory)

    base_date = datetime(2024, 1, 1)

    dummy_trade = DummyTrade(
        product_type=ProductType.FX_SPOT,
        trade_date=base_date,
    )

    monkeypatch.setattr(random, "choice", lambda _: ProductType.FX_SPOT)
    monkeypatch.setattr(factory, "create", lambda pt: dummy_trade)

    trades = service.create_trades(
        n=2,
        product_types=[ProductType.FX_SPOT],
        sort=False,
    )

    assert len(trades) == 2
    assert all(t.product_type == ProductType.FX_SPOT for t in trades)


def test_create_trades_with_sort_false_preserves_creation_order(monkeypatch):
    factory = TradeFactory()
    service = TradeService(factory)

    base_date = datetime(2024, 1, 1)
    trade_dates = [
        base_date,
        base_date + timedelta(days=1),
        base_date + timedelta(days=2),
    ]

    mapping = {
        ProductType.FX_OPTION: DummyTrade(
            product_type=ProductType.FX_OPTION,
            trade_date=trade_dates[0],
        ),
        ProductType.FX_SPOT: DummyTrade(
            product_type=ProductType.FX_SPOT,
            trade_date=trade_dates[1],
        ),
        ProductType.IR_SWAP: DummyTrade(
            product_type=ProductType.IR_SWAP,
            trade_date=trade_dates[2],
        ),
    }

    selected_types = list(mapping.keys())
    sequence = iter(selected_types)

    monkeypatch.setattr(random, "choice", lambda _: next(sequence))
    monkeypatch.setattr(factory, "create", lambda pt: mapping[pt])

    trades = service.create_trades(
        n=3,
        product_types=selected_types,
        sort=False,
    )

    assert [t.product_type for t in trades] == selected_types
    assert [t.trade_date for t in trades] == trade_dates

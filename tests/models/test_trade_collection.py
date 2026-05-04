import pandas as pd

from src.models.trade_collection import TradeCollection
from tests.utils import DummyTrade


def test_to_dicts_returns_underlying_payloads():
    trades = TradeCollection(
        [
            DummyTrade({"trade_id": "T1", "amount": 100}),
            DummyTrade({"trade_id": "T2", "amount": 200}),
        ]
    )

    assert trades.to_dicts() == [
        {"trade_id": "T1", "amount": 100},
        {"trade_id": "T2", "amount": 200},
    ]


def test_to_df_returns_dataframe_with_expected_rows_and_columns():
    trades = TradeCollection(
        [
            DummyTrade({"trade_id": "T1", "amount": 100}),
            DummyTrade({"trade_id": "T2", "amount": 200}),
        ]
    )

    df = trades.to_df()

    assert isinstance(df, pd.DataFrame)
    assert df.to_dict(orient="records") == [
        {"trade_id": "T1", "amount": 100},
        {"trade_id": "T2", "amount": 200},
    ]


def test_to_csv_writes_expected_csv_file(tmp_path):
    trades = TradeCollection(
        [
            DummyTrade({"trade_id": "T1", "amount": 100}),
            DummyTrade({"trade_id": "T2", "amount": 200}),
        ]
    )

    file_path = tmp_path / "trades.csv"
    trades.to_csv(file_path)

    result = pd.read_csv(file_path)
    assert result.to_dict(orient="records") == [
        {"trade_id": "T1", "amount": 100},
        {"trade_id": "T2", "amount": 200},
    ]

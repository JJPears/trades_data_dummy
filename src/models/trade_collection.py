import pandas as pd
from typing import Any

from src.common.utils import validate_csv_file_path


class TradeCollection(list):
    def to_df(self) -> pd.DataFrame:
        rows = [t.model_dump() for t in self]
        return pd.DataFrame(rows)

    def to_dicts(self) -> list[dict[str, Any]]:
        return [t.model_dump() for t in self]

    def to_csv(self, file_path):
        
        validate_csv_file_path(file_path)

        df = self.to_df()
        df.to_csv(file_path, index=False)

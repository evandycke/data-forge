from __future__ import annotations

from collections.abc import Iterator

import pandas as pd


def read_excel_records(file_path: str) -> Iterator[dict[str, object]]:
    workbook = pd.read_excel(file_path, sheet_name=None)

    for sheet_name, dataframe in workbook.items():
        normalized = dataframe.fillna("").to_dict(orient="records")
        for row in normalized:
            yield {
                "_sheet_name": sheet_name,
                **row,
            }

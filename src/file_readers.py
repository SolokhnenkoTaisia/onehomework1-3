"""Модуль для чтения финансовых операций из CSV- и Excel-файлов."""

from pathlib import Path
from typing import Any, cast

import pandas as pd


def read_transactions_from_csv(
    file_path: str | Path,
) -> list[dict[str, Any]]:
    """Читает финансовые операции из CSV-файла и возвращает список словарей."""
    dataframe = pd.read_csv(file_path)
    records = dataframe.to_dict(orient="records")
    return cast(list[dict[str, Any]], records)


def read_transactions_from_excel(
    file_path: str | Path,
) -> list[dict[str, Any]]:
    """Читает финансовые операции из Excel-файла и возвращает
    список словарей."""
    dataframe = pd.read_excel(file_path)
    records = dataframe.to_dict(orient="records")
    return cast(list[dict[str, Any]], records)

"""Тесты для функций чтения CSV- и Excel-файлов."""

from unittest.mock import Mock, patch

from src.file_readers import (
    read_transactions_from_csv,
    read_transactions_from_excel,
)


@patch("src.file_readers.pd.read_csv")
def test_read_transactions_from_csv(mock_read_csv: Mock) -> None:
    """Проверяет чтение CSV-файла."""
    expected = [
        {"id": 1, "state": "EXECUTED", "amount": 100},
        {"id": 2, "state": "CANCELED", "amount": 200},
    ]

    mock_dataframe = Mock()
    mock_dataframe.to_dict.return_value = expected
    mock_read_csv.return_value = mock_dataframe

    result = read_transactions_from_csv("test.csv")

    mock_read_csv.assert_called_once_with(
        "test.csv",
        delimiter=";",
    )
    mock_dataframe.to_dict.assert_called_once_with(orient="records")
    assert result == expected


@patch("src.file_readers.pd.read_excel")
def test_read_transactions_from_excel(mock_read_excel: Mock) -> None:
    """Проверяет чтение Excel-файла."""
    expected = [
        {"id": 1, "state": "EXECUTED", "amount": 300},
        {"id": 2, "state": "CANCELED", "amount": 400},
    ]

    mock_dataframe = Mock()
    mock_dataframe.to_dict.return_value = expected
    mock_read_excel.return_value = mock_dataframe

    result = read_transactions_from_excel("test.xlsx")

    mock_read_excel.assert_called_once_with("test.xlsx")
    mock_dataframe.to_dict.assert_called_once_with(orient="records")
    assert result == expected

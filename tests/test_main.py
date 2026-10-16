"""Тесты главного модуля программы."""

from typing import Any
from unittest.mock import patch

import pytest

from src.main import (
    format_date,
    format_transaction,
    get_amount_and_currency,
    get_currency_code,
    load_transactions,
    main,
)


@pytest.mark.parametrize(
    ("date_value", "expected"),
    [
        ("2019-08-26T10:50:58.294041", "26.08.2019"),
        ("2023-09-05T11:30:32Z", "05.09.2023"),
        ("неверная дата", "неверная дата"),
        ("", "Дата неизвестна"),
    ],
)
def test_format_date(date_value: str, expected: str) -> None:
    """Проверяет форматирование даты."""
    assert format_date(date_value) == expected


def test_get_currency_code_json() -> None:
    """Проверяет получение валюты из JSON."""
    transaction = {
        "operationAmount": {
            "amount": "100.50",
            "currency": {"name": "руб.", "code": "RUB"},
        }
    }
    assert get_currency_code(transaction) == "RUB"


def test_get_currency_code_csv() -> None:
    """Проверяет получение валюты из CSV."""
    assert get_currency_code({"currency_code": "USD"}) == "USD"


def test_get_amount_and_currency_json() -> None:
    """Проверяет получение суммы и валюты из JSON."""
    transaction = {
        "operationAmount": {
            "amount": "100.50",
            "currency": {"name": "руб.", "code": "RUB"},
        }
    }
    assert get_amount_and_currency(transaction) == ("100.50", "руб.")


def test_get_amount_and_currency_csv() -> None:
    """Проверяет получение суммы и валюты из CSV."""
    transaction = {"amount": 200, "currency_name": "Peso"}
    assert get_amount_and_currency(transaction) == ("200", "Peso")


def test_format_transaction() -> None:
    """Проверяет форматирование банковской операции."""
    transaction = {
        "date": "2019-08-26T10:50:58",
        "description": "Перевод организации",
        "from": "Карта 1234",
        "to": "Счет 5678",
        "operationAmount": {
            "amount": "100.00",
            "currency": {"name": "руб.", "code": "RUB"},
        },
    }

    result = format_transaction(transaction)

    assert "26.08.2019 Перевод организации" in result
    assert "Карта 1234 -> Счет 5678" in result
    assert "Сумма: 100.00 руб." in result


@pytest.mark.parametrize(
    ("choice", "expected_reader"),
    [
        ("1", "json"),
        ("2", "csv"),
        ("3", "excel"),
    ],
)
def test_load_transactions(choice: str, expected_reader: str) -> None:
    """Проверяет выбор загрузчика данных."""
    sample: list[dict[str, Any]] = [{"id": 1}]

    with (
        patch("src.main.read_json_file", return_value=sample) as json_reader,
        patch("src.main.read_transactions_from_csv", return_value=sample) as csv_reader,
        patch(
            "src.main.read_transactions_from_excel", return_value=sample
        ) as excel_reader,
    ):
        result = load_transactions(choice)

    assert result == sample
    readers = {"json": json_reader, "csv": csv_reader, "excel": excel_reader}
    readers[expected_reader].assert_called_once()


def test_main_empty_file() -> None:
    """Проверяет обработку пустого списка операций."""
    with (
        patch("builtins.input", side_effect=["2"]),
        patch("src.main.load_transactions", return_value=[]),
        patch("builtins.print") as mock_print,
    ):
        main()

    assert any("пуст" in str(call).lower() for call in mock_print.call_args_list)


def test_main_invalid_file_choice() -> None:
    """Проверяет повторный запрос при неправильном выборе файла."""
    transactions = [
        {"state": "EXECUTED", "date": "2023-01-01", "description": "Перевод"}
    ]

    with (
        patch(
            "builtins.input", side_effect=["9", "2", "EXECUTED", "нет", "нет", "нет"]
        ),
        patch("src.main.load_transactions", return_value=transactions),
        patch("builtins.print") as mock_print,
    ):
        main()

    assert any("Некорректный выбор" in str(call) for call in mock_print.call_args_list)


def test_main_invalid_status() -> None:
    """Проверяет повторный запрос при неправильном статусе."""
    transactions = [
        {"state": "EXECUTED", "date": "2023-01-01", "description": "Перевод"}
    ]

    with (
        patch(
            "builtins.input",
            side_effect=["2", "UNKNOWN", "executed", "нет", "нет", "нет"],
        ),
        patch("src.main.load_transactions", return_value=transactions),
        patch("builtins.print") as mock_print,
    ):
        main()

    assert any(
        "Статус указан неверно" in str(call) for call in mock_print.call_args_list
    )


def test_main_search_and_rub_filter() -> None:
    """Проверяет фильтрацию по рублям и описанию."""
    transactions = [
        {
            "state": "EXECUTED",
            "date": "2023-01-01",
            "description": "Перевод организации",
            "currency_code": "RUB",
            "currency_name": "руб.",
            "amount": 100,
        },
        {
            "state": "EXECUTED",
            "date": "2023-01-02",
            "description": "Открытие вклада",
            "currency_code": "USD",
            "currency_name": "USD",
            "amount": 200,
        },
    ]

    with (
        patch(
            "builtins.input",
            side_effect=["2", "EXECUTED", "нет", "да", "да", "перевод"],
        ),
        patch("src.main.load_transactions", return_value=transactions),
        patch("builtins.print") as mock_print,
    ):
        main()

    output = "\n".join(str(call) for call in mock_print.call_args_list)
    assert "Перевод организации" in output
    assert "Открытие вклада" not in output
    assert "Всего операций: 1" in output


def test_main_no_matching_operations() -> None:
    """Проверяет сообщение, если операции не найдены."""
    transactions = [
        {"state": "EXECUTED", "date": "2023-01-01", "description": "Перевод"}
    ]

    with (
        patch("builtins.input", side_effect=["2", "CANCELED", "нет", "нет", "нет"]),
        patch("src.main.load_transactions", return_value=transactions),
        patch("builtins.print") as mock_print,
    ):
        main()

    assert any(
        "Не найдено ни одной операции" in str(call)
        for call in mock_print.call_args_list
    )

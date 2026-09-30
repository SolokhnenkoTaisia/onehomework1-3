import pytest

from src.generators import (
    card_number_generator,
    filter_by_currency,
    transaction_descriptions,
)


@pytest.fixture
def transactions():
    """Возвращает список тестовых транзакций."""
    return [
        {
            "id": 1,
            "description": "Перевод организации",
            "operationAmount": {
                "amount": "100.00",
                "currency": {"code": "USD"},
            },
        },
        {
            "id": 2,
            "description": "Перевод с карты на карту",
            "operationAmount": {
                "amount": "200.00",
                "currency": {"code": "RUB"},
            },
        },
        {
            "id": 3,
            "description": "Оплата услуг",
            "operationAmount": {
                "amount": "300.00",
                "currency": {"code": "USD"},
            },
        },
    ]


@pytest.mark.parametrize(
    "currency, expected_ids",
    [
        ("USD", [1, 3]),
        ("RUB", [2]),
        ("EUR", []),
    ],
)
def test_filter_by_currency(transactions, currency, expected_ids):
    """Проверяет фильтрацию транзакций по валюте."""
    result = list(filter_by_currency(transactions, currency))
    assert [transaction["id"] for transaction in result] == expected_ids


def test_transaction_descriptions(transactions):
    """Проверяет получение описаний транзакций."""
    result = list(transaction_descriptions(transactions))

    assert result == [
        "Перевод организации",
        "Перевод с карты на карту",
        "Оплата услуг",
    ]


@pytest.mark.parametrize(
    "start, stop, expected",
    [
        (
            1,
            3,
            [
                "0000 0000 0000 0001",
                "0000 0000 0000 0002",
                "0000 0000 0000 0003",
            ],
        ),
        (
            9999999999999998,
            9999999999999999,
            [
                "9999 9999 9999 9998",
                "9999 9999 9999 9999",
            ],
        ),
        (5, 5, ["0000 0000 0000 0005"]),
    ],
)
def test_card_number_generator(start, stop, expected):
    """Проверяет генерацию номеров карт."""
    assert list(card_number_generator(start, stop)) == expected

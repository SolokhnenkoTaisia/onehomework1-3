"""Тесты поиска банковских операций и подсчёта категорий."""

import pytest

from src.search import process_bank_operations, process_bank_search


@pytest.fixture
def transactions() -> list[dict[str, object]]:
    """Возвращает список тестовых банковских операций."""
    return [
        {"id": 1, "description": "Перевод организации"},
        {"id": 2, "description": "Перевод с карты на карту"},
        {"id": 3, "description": "Открытие вклада"},
        {"id": 4, "description": "перевод организации"},
        {"id": 5, "amount": 100},
    ]


@pytest.mark.parametrize(
    ("search", "expected_ids"),
    [
        ("Перевод", [1, 2, 4]),
        ("ОРГАНИЗАЦИИ", [1, 4]),
        ("вклад", [3]),
        ("несуществующая операция", []),
        ("", [1, 2, 3, 4]),
    ],
)
def test_process_bank_search(
    transactions: list[dict[str, object]],
    search: str,
    expected_ids: list[int],
) -> None:
    """Проверяет поиск по описанию с учётом регистра."""
    result = process_bank_search(transactions, search)

    assert [item["id"] for item in result] == expected_ids


def test_process_bank_search_literal_regex(
    transactions: list[dict[str, object]],
) -> None:
    """Проверяет, что специальные символы ищутся буквально."""
    transactions.append({"id": 6, "description": "Платёж."})

    result = process_bank_search(transactions, "платёж.")

    assert [item["id"] for item in result] == [6]


def test_process_bank_search_empty_data() -> None:
    """Проверяет поиск в пустом списке."""
    assert process_bank_search([], "перевод") == []


def test_process_bank_operations(
    transactions: list[dict[str, object]],
) -> None:
    """Проверяет подсчёт операций по категориям."""
    categories = [
        "Перевод организации",
        "Перевод с карты на карту",
        "Открытие вклада",
        "Несуществующая категория",
    ]

    result = process_bank_operations(transactions, categories)

    assert result == {
        "Перевод организации": 1,
        "Перевод с карты на карту": 1,
        "Открытие вклада": 1,
        "Несуществующая категория": 0,
    }


def test_process_bank_operations_empty_data() -> None:
    """Проверяет подсчёт категорий для пустого списка."""
    assert process_bank_operations([], ["Перевод", "Вклад"]) == {
        "Перевод": 0,
        "Вклад": 0,
    }


def test_process_bank_operations_empty_categories(
    transactions: list[dict[str, object]],
) -> None:
    """Проверяет подсчёт при отсутствии заданных категорий."""
    assert process_bank_operations(transactions, []) == {}

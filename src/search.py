"""Модуль поиска банковских операций и подсчёта категорий."""

import re
from collections import Counter
from typing import Any


def process_bank_search(
    data: list[dict[str, Any]], search: str
) -> list[dict[str, Any]]:
    """Ищет операции, в описании которых содержится заданная строка.

    Поиск выполняется без учёта регистра. Введённая строка рассматривается
    как обычный текст, а не как шаблон регулярного выражения.

    Args:
        data: Список банковских операций.
        search: Строка для поиска в поле description.

    Returns:
        Список операций, описания которых содержат строку поиска.
    """
    pattern = re.compile(re.escape(search), re.IGNORECASE)

    return [
        transaction
        for transaction in data
        if isinstance(transaction.get("description"), str)
        and pattern.search(transaction["description"])
    ]


def process_bank_operations(
    data: list[dict[str, Any]], categories: list[str]
) -> dict[str, int]:
    """Подсчитывает количество операций для каждой заданной категории.

    Категория определяется по точному совпадению с полем description.

    Args:
        data: Список банковских операций.
        categories: Названия категорий для подсчёта.

    Returns:
        Словарь, где ключи — категории, а значения — количество операций.
        Для категории без совпадений возвращается ноль.
    """
    category_counts: Counter[str] = Counter({category: 0 for category in categories})

    descriptions = (
        transaction["description"]
        for transaction in data
        if isinstance(transaction.get("description"), str)
    )

    category_counts.update(
        description for description in descriptions if description in category_counts
    )

    return dict(category_counts)

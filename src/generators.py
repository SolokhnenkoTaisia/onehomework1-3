from collections.abc import Iterator
from typing import Any


def filter_by_currency(
    transactions: list[dict[str, Any]], currency: str
) -> Iterator[dict[str, Any]]:
    """Возвращает транзакции, у которых совпадает код валюты."""
    for transaction in transactions:
        operation_amount = transaction.get("operationAmount", {})
        currency_info = operation_amount.get("currency", {})
        currency_code = currency_info.get("code")

        if currency_code == currency:
            yield transaction


def transaction_descriptions(
    transactions: list[dict[str, Any]],
) -> Iterator[str]:
    """По очереди возвращает описания транзакций."""
    for transaction in transactions:
        yield transaction["description"]


def card_number_generator(start: int, stop: int) -> Iterator[str]:
    """Генерирует номера карт в заданном диапазоне."""
    for number in range(start, stop + 1):
        yield f"{number:016d}"[:4] + " " + f"{number:016d}"[4:8] + " " + (
            f"{number:016d}"[8:12]
        ) + " " + f"{number:016d}"[12:]

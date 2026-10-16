"""Главный модуль программы для работы с банковскими операциями."""

from datetime import datetime
from pathlib import Path
from typing import Any

from src.file_readers import (
    read_transactions_from_csv,
    read_transactions_from_excel,
)
from src.processing import filter_by_state, sort_by_date
from src.search import process_bank_search
from src.utils import read_json_file

DATA_DIR = Path(__file__).resolve().parent.parent / "data"

FILE_PATHS = {
    "1": DATA_DIR / "operations.json",
    "2": DATA_DIR / "transactions.csv",
    "3": DATA_DIR / "transactions_excel.xlsx",
}


def load_transactions(file_choice: str) -> list[dict[str, Any]]:
    """Загружает операции из выбранного файла."""
    file_path = FILE_PATHS[file_choice]

    if file_choice == "1":
        return read_json_file(str(file_path))
    if file_choice == "2":
        return read_transactions_from_csv(str(file_path))
    return read_transactions_from_excel(str(file_path))


def get_currency_code(transaction: dict[str, Any]) -> str:
    """Возвращает код валюты операции для любого поддерживаемого формата."""
    operation_amount = transaction.get("operationAmount")

    if isinstance(operation_amount, dict):
        currency = operation_amount.get("currency", {})
        if isinstance(currency, dict):
            return str(currency.get("code", ""))

    return str(transaction.get("currency_code", ""))


def get_amount_and_currency(
    transaction: dict[str, Any],
) -> tuple[str, str]:
    """Возвращает сумму и валюту операции."""
    operation_amount = transaction.get("operationAmount")

    if isinstance(operation_amount, dict):
        currency = operation_amount.get("currency", {})
        amount = operation_amount.get("amount", "0")
        if isinstance(currency, dict):
            currency_name = currency.get("name", currency.get("code", ""))
        else:
            currency_name = ""
        return str(amount), str(currency_name)

    amount = transaction.get("amount", "0")
    currency_name = transaction.get(
        "currency_name", transaction.get("currency_code", "")
    )
    return str(amount), str(currency_name)


def format_date(date_value: Any) -> str:
    """Преобразует дату операции в формат ДД.ММ.ГГГГ."""
    if not date_value:
        return "Дата неизвестна"

    try:
        date_text = str(date_value).replace("Z", "+00:00")
        return datetime.fromisoformat(date_text).strftime("%d.%m.%Y")
    except (ValueError, TypeError):
        return str(date_value)


def format_transaction(transaction: dict[str, Any]) -> str:
    """Форматирует одну банковскую операцию для вывода."""
    date = format_date(transaction.get("date", ""))
    description = transaction.get("description", "Без описания")
    sender = transaction.get("from", "")
    recipient = transaction.get("to", "")
    amount, currency = get_amount_and_currency(transaction)

    transfer = ""
    if sender:
        transfer = str(sender)
    if recipient:
        transfer = f"{transfer} -> {recipient}" if transfer else str(recipient)

    lines = [
        f"{date} {description}",
        transfer,
        f"Сумма: {amount} {currency}".strip(),
    ]
    return "\n".join(line for line in lines if line)


def main() -> None:
    """Запускает интерактивную обработку банковских операций."""
    print("Привет! Добро пожаловать в программу работы с банковскими операциями.")
    print("Выберите источник данных:")
    print("1. JSON")
    print("2. CSV")
    print("3. Excel")

    file_choice = input("Введите номер источника данных: ").strip()
    while file_choice not in FILE_PATHS:
        print("Некорректный выбор. Введите 1, 2 или 3.")
        file_choice = input("Введите номер источника данных: ").strip()

    transactions = load_transactions(file_choice)
    if not transactions:
        print("Не удалось загрузить операции или список операций пуст.")
        return

    valid_statuses = {"EXECUTED", "CANCELED", "PENDING"}
    status = (
        input("Введите статус операции (EXECUTED, CANCELED, PENDING): ").strip().upper()
    )

    while status not in valid_statuses:
        print("Статус указан неверно.")
        status = (
            input("Введите статус операции (EXECUTED, CANCELED, PENDING): ")
            .strip()
            .upper()
        )

    # Нормализуем статус для фильтрации независимо от регистра.
    filtered_transactions = filter_by_state(transactions, state=status)

    sort_answer = input("Отсортировать операции по дате? (да/нет): ").strip().lower()
    if sort_answer in {"да", "д", "yes", "y"}:
        order = input("Сортировать по возрастанию или убыванию? ").strip().lower()
        reverse = order not in {"по возрастанию", "возрастание", "asc", "ascending"}
        filtered_transactions = sort_by_date(filtered_transactions, reverse=reverse)

    rub_answer = input("Выводить только операции в рублях? (да/нет): ").strip().lower()
    if rub_answer in {"да", "д", "yes", "y"}:
        filtered_transactions = [
            transaction
            for transaction in filtered_transactions
            if get_currency_code(transaction).upper() == "RUB"
        ]

    search_answer = (
        input("Отфильтровать операции по описанию? (да/нет): ").strip().lower()
    )
    if search_answer in {"да", "д", "yes", "y"}:
        search_text = input("Введите слово для поиска в описании: ").strip()
        filtered_transactions = process_bank_search(filtered_transactions, search_text)

    if not filtered_transactions:
        print("Не найдено ни одной операции, подходящей под ваши условия.")
        return

    print("\nСписок банковских операций:")
    for transaction in filtered_transactions:
        print(format_transaction(transaction))
        print("-" * 40)

    print(f"Всего операций: {len(filtered_transactions)}")


if __name__ == "__main__":
    main()

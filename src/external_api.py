import os
from typing import Any

import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("EXCHANGE_API_KEY")
API_URL = "https://api.apilayer.com/exchangerates_data/convert"


def convert_amount_to_rub(transaction: dict[str, Any]) -> float:
    """Конвертирует сумму транзакции в рубли."""
    amount = float(transaction["operationAmount"]["amount"])
    currency = transaction["operationAmount"]["currency"]["code"]

    if currency == "RUB":
        return amount

    if currency not in ("USD", "EUR"):
        raise ValueError(f"Неподдерживаемая валюта: {currency}")

    if not API_KEY:
        raise ValueError("Не задан API-ключ в файле .env")

    response = requests.get(
        API_URL,
        headers={"apikey": API_KEY},
        params={
            "to": "RUB",
            "from": currency,
            "amount": amount,
        },
        timeout=10,
    )
    response.raise_for_status()

    return float(response.json()["result"])

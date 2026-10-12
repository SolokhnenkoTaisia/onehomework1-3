from unittest.mock import Mock, patch

import pytest

from src.external_api import convert_amount_to_rub


def make_transaction(amount: str, currency: str) -> dict:
    """Создаёт тестовую транзакцию."""
    return {
        "operationAmount": {
            "amount": amount,
            "currency": {
                "name": currency,
                "code": currency,
            },
        }
    }


def test_convert_rub_without_api() -> None:
    """Проверяет, что рублёвая сумма возвращается без API-запроса."""
    transaction = make_transaction("1500.50", "RUB")

    with patch("src.external_api.requests.get") as mock_get:
        result = convert_amount_to_rub(transaction)

    assert result == 1500.50
    assert isinstance(result, float)
    mock_get.assert_not_called()


@pytest.mark.parametrize(
    ("currency", "amount", "converted_amount"),
    [
        ("USD", "10.00", 800.0),
        ("EUR", "20.00", 1800.0),
    ],
)
def test_convert_foreign_currency(
    currency: str,
    amount: str,
    converted_amount: float,
) -> None:
    """Проверяет конвертацию USD и EUR с имитацией ответа API."""
    transaction = make_transaction(amount, currency)
    mock_response = Mock()
    mock_response.json.return_value = {"result": converted_amount}
    mock_response.raise_for_status.return_value = None

    with (
        patch("src.external_api.API_KEY", "test_api_key"),
        patch(
            "src.external_api.requests.get",
            return_value=mock_response,
        ) as mock_get,
    ):
        result = convert_amount_to_rub(transaction)

    assert result == converted_amount
    assert isinstance(result, float)
    mock_get.assert_called_once_with(
        "https://api.apilayer.com/exchangerates_data/convert",
        headers={"apikey": "test_api_key"},
        params={
            "to": "RUB",
            "from": currency,
            "amount": float(amount),
        },
        timeout=10,
    )


def test_convert_without_api_key() -> None:
    """Проверяет ошибку, если API-ключ не задан."""
    transaction = make_transaction("10.00", "USD")

    with (
        patch("src.external_api.API_KEY", None),
        pytest.raises(ValueError, match="API-ключ"),
        patch("src.external_api.requests.get") as mock_get,
    ):
        convert_amount_to_rub(transaction)

    mock_get.assert_not_called()


def test_convert_unsupported_currency() -> None:
    """Проверяет обработку неподдерживаемой валюты."""
    transaction = make_transaction("10.00", "CNY")

    with pytest.raises(ValueError, match="Неподдерживаемая валюта"):
        convert_amount_to_rub(transaction)


def test_convert_api_error() -> None:
    """Проверяет обработку ошибки ответа API."""
    transaction = make_transaction("10.00", "USD")
    mock_response = Mock()
    mock_response.raise_for_status.side_effect = Exception("API error")

    with (
        patch("src.external_api.API_KEY", "test_api_key"),
        patch(
            "src.external_api.requests.get",
            return_value=mock_response,
        ),
        pytest.raises(Exception, match="API error"),
    ):
        convert_amount_to_rub(transaction)

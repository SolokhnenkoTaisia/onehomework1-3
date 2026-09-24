import pytest

from src.widget import get_date, mask_account_card


@pytest.mark.parametrize(
    "info, expected",
    [
        ("Visa 1234567890123456", "Visa 1234 56** **** 3456"),
        ("MasterCard 5555555555554444", "MasterCard 5555 55** **** 4444"),
        ("Счет 1234567890", "Счет **7890"),
    ],
)
def test_mask_account_card(info, expected):
    assert mask_account_card(info) == expected


@pytest.mark.parametrize(
    "info",
    [
        "",
        "1234567890",
        "Visa abcdefgh",
    ],
)
def test_mask_account_card_invalid(info):
    assert mask_account_card(info) == "Некорректный ввод"


@pytest.mark.parametrize(
    "date, expected",
    [
        ("2024-01-15T10:30:00", "15.01.2024"),
        ("2023-12-31T23:59:59", "31.12.2023"),
        ("2025-06-01T08:00:00", "01.06.2025"),
    ],
)
def test_get_date(date, expected):
    assert get_date(date) == expected
import pytest

from src.masks import get_mask_account, get_mask_card_number


@pytest.mark.parametrize(
    "card_number, expected",
    [
        ("1234567890123456", "1234 56** **** 3456"),
        ("5555555555554444", "5555 55** **** 4444"),
        ("1111222233334444", "1111 22** **** 4444"),
    ],
)
def test_get_mask_card_number(card_number, expected):
    assert get_mask_card_number(card_number) == expected


@pytest.mark.parametrize(
    "account_number, expected",
    [
        ("1234567890", "**7890"),
        ("5555555555", "**5555"),
        ("1111222233", "**2233"),
    ],
)
def test_get_mask_account(account_number, expected):
    assert get_mask_account(account_number) == expected
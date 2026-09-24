import pytest

from src.processing import filter_by_state, sort_by_date


@pytest.fixture
def operations():
    return [
        {"id": 1, "state": "EXECUTED", "date": "2024-03-20"},
        {"id": 2, "state": "CANCELED", "date": "2024-01-15"},
        {"id": 3, "state": "EXECUTED", "date": "2024-02-10"},
        {"id": 4, "state": "PENDING", "date": "2024-04-05"},
    ]


@pytest.mark.parametrize(
    "state, expected_ids",
    [
        ("EXECUTED", [1, 3]),
        ("CANCELED", [2]),
        ("PENDING", [4]),
    ],
)
def test_filter_by_state(operations, state, expected_ids):
    result = filter_by_state(operations, state)

    assert [item["id"] for item in result] == expected_ids


def test_filter_by_state_default(operations):
    result = filter_by_state(operations)

    assert [item["id"] for item in result] == [1, 3]


@pytest.mark.parametrize(
    "reverse, expected_ids",
    [
        (True, [4, 1, 3, 2]),
        (False, [2, 3, 1, 4]),
    ],
)
def test_sort_by_date(operations, reverse, expected_ids):
    result = sort_by_date(operations, reverse)

    assert [item["id"] for item in result] == expected_ids


def test_sort_by_date_does_not_change_original(operations):
    original = operations.copy()

    sort_by_date(operations)

    assert operations == original
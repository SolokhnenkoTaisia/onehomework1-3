import json
from unittest.mock import mock_open, patch

import pytest

from src.utils import read_json_file


def test_read_json_file_success() -> None:
    """Проверяет чтение списка словарей из JSON."""
    json_data = [
        {"id": 1, "amount": 100},
        {"id": 2, "amount": 200},
    ]
    mocked_file = mock_open(read_data=json.dumps(json_data))

    with patch("builtins.open", mocked_file):
        result = read_json_file("test.json")

    assert result == json_data
    mocked_file.assert_called_once_with("test.json", encoding="utf-8")


@pytest.mark.parametrize(
    "content",
    [
        "",
        "{invalid json}",
        '{"id": 1}',
        "123",
        '"text"',
        "null",
    ],
)
def test_read_json_file_invalid_content(content: str) -> None:
    """Проверяет пустой файл, неправильный JSON и содержимое,
    не в виде списка."""
    mocked_file = mock_open(read_data=content)

    with patch("builtins.open", mocked_file):
        result = read_json_file("test.json")

    assert result == []


def test_read_json_file_filters_non_dict_items() -> None:
    """Проверяет, что в результате остаются только словари."""
    content = json.dumps([{"id": 1}, "text", 123, None, {"id": 2}])
    mocked_file = mock_open(read_data=content)

    with patch("builtins.open", mocked_file):
        result = read_json_file("test.json")

    assert result == [{"id": 1}, {"id": 2}]


def test_read_json_file_not_found() -> None:
    """Проверяет возврат пустого списка, если файл не найден."""
    with patch("builtins.open", side_effect=FileNotFoundError):
        result = read_json_file("missing.json")

    assert result == []


def test_read_json_file_os_error() -> None:
    """Проверяет обработку ошибки доступа к файлу."""
    with patch("builtins.open", side_effect=OSError):
        result = read_json_file("unavailable.json")

    assert result == []

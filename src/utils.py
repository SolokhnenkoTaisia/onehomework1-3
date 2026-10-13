import json
from pathlib import Path
from typing import Any


def read_json_file(file_path: str | Path) -> list[dict[str, Any]]:
    """Читает JSON-файл и возвращает список словарей с данными."""
    try:
        with open(file_path, encoding="utf-8") as file:
            data = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return []

    if isinstance(data, list):
        return [item for item in data if isinstance(item, dict)]

    return []

import json
import logging
from pathlib import Path
from typing import Any

LOG_DIR = Path(__file__).resolve().parent.parent / "logs"
LOG_DIR.mkdir(exist_ok=True)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

file_handler = logging.FileHandler(
    LOG_DIR / "utils.log",
    mode="w",
    encoding="utf-8",
)
file_formatter = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)


def read_json_file(file_path: str | Path) -> list[dict[str, Any]]:
    """Читает JSON-файл и возвращает список словарей с данными."""
    try:
        with open(file_path, encoding="utf-8") as file:
            data = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError, OSError) as error:
        logger.error("Не удалось прочитать файл %s: %s", file_path, error)
        return []

    if not isinstance(data, list):
        logger.error("Файл %s не содержит список JSON-объектов", file_path)
        return []

    result = [item for item in data if isinstance(item, dict)]
    logger.info("Файл %s успешно прочитан", file_path)
    return result

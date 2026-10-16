import logging
from pathlib import Path

LOG_DIR = Path(__file__).resolve().parent.parent / "logs"
LOG_DIR.mkdir(exist_ok=True)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

file_handler = logging.FileHandler(
    LOG_DIR / "masks.log",
    mode="w",
    encoding="utf-8",
)
file_formatter = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)


def get_mask_card_number(card_number: str) -> str:
    """Маскирует номер банковской карты."""
    try:
        first_part = f"{card_number[:4]} {card_number[4:6]}** ****"
        last_four = card_number[-4:]
        result = f"{first_part} {last_four}"
        logger.info("Номер карты успешно замаскирован")
        return result
    except Exception as error:
        logger.error("Ошибка при маскировке номера карты: %s", error)
        raise


def get_mask_account(account_number: str) -> str:
    """Маскирует номер банковского счета."""
    try:
        result = f"**{account_number[-4:]}"
        logger.info("Номер счета успешно замаскирован")
        return result
    except Exception as error:
        logger.error("Ошибка при маскировке номера счета: %s", error)
        raise

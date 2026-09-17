from datetime import datetime

from src.masks import get_mask_account, get_mask_card_number


def mask_account_card(info: str) -> str:
    """Маскирует номер банковской карты или счета."""
    parts = info.split()

    if not parts:
        return "Некорректный ввод"

    number = parts[-1]
    name = " ".join(parts[:-1])

    if not number.isdigit():
        return "Некорректный ввод"

    if not name:
        return "Некорректный ввод"

    if name.lower() == "счет":
        masked_number = get_mask_account(number)
    else:
        masked_number = get_mask_card_number(number)

    return f"{name} {masked_number}"


def get_date(date: str) -> str:
    """Преобразует дату из ISO-формата в ДД.ММ.ГГГГ."""
    date_obj = datetime.fromisoformat(date)
    return date_obj.strftime("%d.%m.%Y")

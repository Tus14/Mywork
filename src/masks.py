import logging
from pathlib import Path
from typing import Union

# Путь к папке logs
LOGS_DIR = Path(__file__).parent.parent / "logs"
LOGS_DIR.mkdir(exist_ok=True)

# Настройка логгера с UTF-8 кодировкой
logger = logging.getLogger("masks")
logger.setLevel(logging.DEBUG)

# Создаем handler с явным указанием UTF-8
file_handler = logging.FileHandler(LOGS_DIR / "masks.log", mode="w", encoding="utf-8")  # ← Добавляем эту строку
file_handler.setLevel(logging.DEBUG)

# Форматтер
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)


# Устанавливаю уровень логирования
logger.setLevel(logging.DEBUG)


def get_mask_card_number(card_number: Union[int, str]) -> Union[int, str]:
    """Принимает номер карты и возвращает его маскированную версию."""
    try:
        card_number = str(card_number)
        card_number = card_number.replace(" ", "")

        if len(card_number) < 16:
            raise ValueError("Номер карты слишком короткий")

        first_digit = card_number[:6]
        last_digit = card_number[-4:]
        masked_cod = "*" * (len(card_number) - 10)
        card_mask = f"{first_digit[:4]} {first_digit[4:]}{masked_cod[:2]} {masked_cod[2:]} {last_digit}"

        logger.debug(f"Успешная маскировка карты. Входные данные: {card_number}, Результат: {card_mask}")
        return card_mask

    except Exception as e:
        logger.error(f"Ошибка при маскировке карты: {str(e)}", exc_info=True)
        raise


def get_mask_account(account_number: Union[int, str]) -> Union[int, str]:
    """Принимает номер счёта и возвращает его маскированную версию."""
    try:
        account_number = str(account_number)

        if len(account_number) < 4:
            raise ValueError("Номер счета слишком короткий")

        last_digit = account_number[-4:]
        account_mask = f"**{last_digit}"

        logger.debug(f"Успешная маскировка счета. Результат: {account_mask}")
        return account_mask

    except Exception as e:
        logger.error(f"Ошибка при маскировке счета: {str(e)}", exc_info=True)
        raise

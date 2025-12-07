import os
import json
from json.decoder import JSONDecodeError
import logging
from typing import List, Dict, Any

# Создаю отдельный логер для модуля utils
logger = logging.getLogger("utils")
# Устанавливаю уровень логирования (не ниже DEBUG)
logger.setLevel(logging.DEBUG)
# Проверяю, чтобы handlers добавлялись только один раз
if not logger.handlers:
    # Простая проверка и создание папки logs
    if not os.path.exists("logs"):
        os.mkdir("logs")

    # Создаем handler для вывода в файл 'logs/utils.log'
    file_handler = logging.FileHandler(
        filename="logs/utils.log", encoding="utf-8", mode="w"  # Файл создается в папке logs
    )
    # Устанавливаю уровень для handler (не ниже DEBUG)
    file_handler.setLevel(logging.DEBUG)
    # Создаю formatter с нужным форматом
    file_formatter = logging.Formatter(
        fmt="%(asctime)s - %(name)s - %(levelname)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
    )
    # Устанавливаю formatter для handler
    file_handler.setFormatter(file_formatter)
    # Добавляю handler к логгеру
    logger.addHandler(file_handler)


def load_transactions(filepath: str) -> List[Dict[str, Any]]:
    """Загружает данные о финансовых транзакциях из JSON-файла."""
    try:
        logger.debug(f"Начало загрузки транзакций из файла: {filepath}")

        with open(filepath, "r", encoding="utf-8") as file:
            content = file.read()
            if not content:
                logger.warning(f"Файл {filepath} пуст")
                return []

            data = json.loads(content)

            if isinstance(data, list):
                logger.info(f"Успешно загружено {len(data)} транзакций из {filepath}")
                return data
            else:
                logger.warning(f"Файл {filepath} содержит данные не в виде списка")
                return []

    except FileNotFoundError:
        logger.error(f"Файл не найден: {filepath}")
        return []
    except JSONDecodeError as e:
        logger.error(f"Ошибка декодирования JSON в файле {filepath}: {str(e)}")
        return []
    except Exception as e:
        logger.error(f"Непредвиденная ошибка при чтении файла {filepath}: {str(e)}", exc_info=True)
        return []

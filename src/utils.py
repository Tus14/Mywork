import json
from json.decoder import JSONDecodeError
from typing import List, Dict, Any


def load_transactions(filepath: str) -> List[Dict[str, Any]]:
    """Загружает данные о финансовых транзакциях из JSON-файла.
    Args:
        filepath: Путь до JSON-файла.
    Returns:
        Список словарей с данными о транзакциях или пустой список в случае
        ошибки (файл не найден, пустой, или содержит данные не в виде списка).
    """
    try:
        with open(filepath, "r", encoding="utf-8") as file:
            # Чтение содержимого файла
            content = file.read()
            if not content:
                # Если файл пустой, возвращаем пустой список
                return []

            # Десериализация JSON-данных
            data = json.loads(content)

            # Проверка, является ли загруженный объект списком
            if isinstance(data, list):
                return data
            else:
                # Если это не список (например, словарь), возвращаем пустой список
                return []

    except FileNotFoundError:
        # Обработка случая, когда файл не найден
        return []
    except JSONDecodeError:
        # Обработка случая, когда файл содержит некорректный JSON
        return []
    except Exception as e:
        # Общая обработка других возможных ошибок
        # Можно добавить логирование ошибки при необходимости
        print(f"Произошла непредвиденная ошибка при чтении файла: {e}")
        return []

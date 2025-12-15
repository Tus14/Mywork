from typing import List, Dict, Any, Iterator


def filter_by_currency(transactions: List[Dict[str, Any]], currency_code: str) -> Iterator[Dict[str, Any]]:
    """Функция фильтрует список операций(транзакций) по заданной валюте и возвращает итератор.
    Аргументы:
        operations: Список словарей, представляющих транзакции.
        currency_code: Требуемый код валюты (например, "USD", "RUB").
    Yields:
        Словарь, представляющий транзакцию в указанной валюте."""
    for transaction in transactions:
        # Пытаемся безопасно извлечь код валюты, проверяя вложенные ключи
        currency = transaction.get("operationAmount", {}).get("currency", {}).get("code")

        # Если currency не None и соответствует искомому коду
        if currency == currency_code:
            yield transaction


def transaction_descriptions(transactions: List[Dict[str, Any]]) -> Iterator[str]:
    """Генератор, который принимает список транзакций и возвращает
    описание каждой операции по очереди. Если описание отсутствует, то выводится 'Описание
    отсутствует'"""
    for transaction in transactions:
        description = transaction.get("description", "Описание отсутствует")
        yield description


def format_card(number: int) -> str:
    """Вспомогательная функция для форматирования одного целого числа в номер карты."""
    padded_number = str(number).zfill(16)
    # Используем " ".join с генераторным выражением для чистоты
    chunks = (padded_number[i: i + 4] for i in range(0, 16, 4))
    return " ".join(chunks)


def card_number_generator(start: int, end: int) -> Iterator[str]:
    """Генератор, использующий map для форматирования диапазона чисел."""
    return map(format_card, range(start, end + 1))

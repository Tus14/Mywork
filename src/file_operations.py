from typing import List, Dict
from .processing import (
    filter_by_state,
    sort_by_date,
    process_bank_search,
    process_bank_operations
)



def filter_transactions_by_status(data: List[Dict], status: str) -> List[Dict]:
    """
    Фильтрует транзакции по статусу

    Args:
        data: Список транзакций
        status: Статус для фильтрации (EXECUTED, CANCELED, PENDING)

    Returns:
        Отфильтрованный список транзакций
    """
    return filter_by_state(data, status)


def sort_transactions_by_date(data: List[Dict], reverse: bool = False) -> List[Dict]:
    """
    Сортирует транзакции по дате

    Args:
        data: Список транзакций
        reverse: Если True - сортировка по убыванию, False - по возрастанию

    Returns:
        Отсортированный список транзакций
    """
    return sort_by_date(data, descending=reverse)


def search_in_transactions(data: List[Dict], search_string: str) -> List[Dict]:
    """
    Ищет транзакции по строке в описании с использованием регулярных выражений

    Args:
        data: Список транзакций
        search_string: Строка для поиска в описании

    Returns:
        Отфильтрованный список транзакций
    """
    return process_bank_search(data, search_string)


def count_transactions_by_categories(data: List[Dict], categories: List[str]) -> Dict[str, int]:
    """
    Подсчитывает количество транзакций по заданным категориям

    Args:
        data: Список транзакций
        categories: Список категорий для поиска в описаниях

    Returns:
        Словарь с количеством операций по каждой категории
    """
    return process_bank_operations(data, categories)


def filter_by_currency(data: List[Dict], currency: str = "RUB") -> List[Dict]:
    """
    Фильтрует транзакции по валюте

    Args:
        data: Список транзакций
        currency: Код валюты (по умолчанию RUB)

    Returns:
        Отфильтрованный список транзакций
    """
    return [t for t in data if t.get("currency", "").upper() == currency.upper()]

import re
from collections import Counter
from typing import List, Dict


def filter_by_state(list_of_dicts: List[Dict], state_value: str = "EXECUTED") -> List[Dict]:
    """Функция, которая принимает список словарей и опционально значение для ключа
    state (по умолчанию 'EXECUTED')"""
    new_list: List[Dict] = []
    for i in list_of_dicts:
        if i.get("state") == state_value:
            new_list.append(i)
    return new_list


def sort_by_date(operations: List[Dict], descending: bool = True) -> List[Dict]:
    """Функция сортирует список словарей по дате, используя несколько строк кода."""
    sorted_operations = operations.copy()

    def get_date_key(item_dict: Dict) -> str:
        return str(item_dict.get("date", ""))

    sorted_operations.sort(key=get_date_key, reverse=descending)
    return sorted_operations


def process_bank_search(data: List[Dict], search: str) -> List[Dict]:
    """
    Фильтрует операции по строке поиска в описании с использованием регулярных выражений.

    Args:
        data: Список словарей с банковскими операциями
        search: Строка для поиска в описании операций

    Returns:
        Список словарей, где в описании найдена искомая строка
    """
    pattern = re.compile(re.escape(search), re.IGNORECASE)
    return [op for op in data if "description" in op and pattern.search(op["description"])]


def process_bank_operations(data: List[Dict], categories: List[str]) -> Dict[str, int]:
    """
    Подсчитывает количество операций по заданным категориям.

    Args:
        data: Список словарей с банковскими операциями
        categories: Список категорий для поиска в описаниях операций

    Returns:
        Словарь с количеством операций по каждой категории
    """
    category_counts: Counter[str] = Counter()

    for op in data:
        if "description" in op:
            description = op["description"].lower()
            for category in categories:
                if category.lower() in description:
                    category_counts[category] += 1

    return dict(category_counts)

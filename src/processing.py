def filter_by_state(list_of_dicts: list, state_value: str = "EXECUTED") -> list:
    """Функция, которая принимает список словарей и опционально значение для ключа
    state (по умолчанию 'EXECUTED')"""
    new_list = []
    for i in list_of_dicts:
        if i.get("state") == state_value:
            new_list.append(i)
    return new_list


def sort_by_date(operations: list, descending: bool = True) -> list:
    """
    Сортирует список словарей по дате, используя несколько строк кода.
    """
    sorted_operations = operations.copy()

    def get_date_key(item_dict: dict) -> str:
        return item_dict["date"]

    sorted_operations.sort(key=get_date_key, reverse=descending)
    return sorted_operations

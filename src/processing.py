def filter_by_state(list_of_dicts: list, state_value: str = 'EXECUTED') -> list:
    """Функция, которая принимает список словарей и опционально значение для ключа
state (по умолчанию 'EXECUTED')"""
    new_list = []
    for i in list_of_dicts:
        if i.get('state') == state_value:
            new_list.append(i)
    return new_list
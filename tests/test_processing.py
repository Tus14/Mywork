import pytest
from typing import Any
from src.processing import filter_by_state, sort_by_date, process_bank_search, process_bank_operations


@pytest.fixture
def sample_data() -> list[dict]:
    """Фикстура, предоставляющая тестовый набор данных."""
    return [
        {"id": 1, "state": "EXECUTED", "amount": 100},
        {"id": 2, "state": "CANCELED", "amount": 200},
        {"id": 3, "state": "EXECUTED", "amount": 300},
        {"id": 4, "state": "CANCELED", "amount": 400},
        {"id": 5, "state": "PENDING", "amount": 500},
    ]


@pytest.mark.parametrize(
    "state_filter, expected_count, expected_ids",
    [
        ("EXECUTED", 2, [1, 3]),
        ("CANCELED", 2, [2, 4]),
    ],
)
def test_filter_by_state_valid(
    sample_data: list[dict], state_filter: str, expected_count: int, expected_ids: list[int]
) -> None:
    """Проверка корректности фильтрации для существующих статусов с использованием параметризации."""
    result = filter_by_state(sample_data, state_filter)

    # Проверка количества отфильтрованных элементов
    assert len(result) == expected_count

    # Проверка, что в результате только ожидаемые ID
    result_ids = [item["id"] for item in result]
    assert result_ids == expected_ids

    # Дополнительная проверка, что все элементы в результате имеют правильный state
    for item in result:
        assert item["state"] == state_filter


def test_filter_by_state_not_found(sample_data: list[dict]) -> None:
    """
    Тестирование случая, когда ни один словарь не соответствует заданному статусу.
    """
    # Статус 'PENDING' есть в данных, но мы ищем 'COMPLETED', которого нет
    result = filter_by_state(sample_data, "COMPLETED")
    assert len(result) == 0
    assert result == []


def test_filter_by_state_empty_list() -> None:
    """Тестирование передачи пустого списка."""
    result = filter_by_state([], "EXECUTED")
    assert len(result) == 0
    assert result == []


@pytest.fixture
def sample_operations() -> list[dict]:
    """Фикстура, предоставляющая тестовый набор операций с разными датами."""
    return [
        {"id": 1, "date": "2023-01-15T10:00:00Z"},
        {"id": 2, "date": "2023-01-10T12:00:00Z"},
        {"id": 3, "date": "2023-01-15T11:00:00Z"},
        {"id": 4, "date": "2022-12-01T09:00:00Z"},
    ]


@pytest.mark.parametrize(
    "descending_flag, expected_order_ids",
    [
        # Добавляем второй элемент (список ID) в кортеж
        (True, [3, 1, 2, 4]),
        # Добавляем второй элемент (список ID) в кортеж
        (False, [4, 2, 1, 3]),
    ],
)
def test_sort_by_date_order(
    sample_operations: list[dict], descending_flag: bool, expected_order_ids: list[int]
) -> None:
    """Тестирование сортировки списка словарей по датам в порядке убывания и возрастания
    с использованием параметризации."""
    result = sort_by_date(sample_operations, descending=descending_flag)

    # Извлекаем ID из отсортированного списка для сравнения с ожидаемым порядком
    result_ids = [op["id"] for op in result]

    assert result_ids == expected_order_ids


def test_sort_by_date_empty_list() -> None:
    """Тестирование обработки пустого списка (должно возвращать пустой список без ошибок)."""
    result = sort_by_date([])
    assert result == []


@pytest.fixture
def operations_with_missing_date_key() -> list[dict]:
    """Фикстура с операциями, одна из которых не имеет ключа 'date'."""
    return [
        {"id": 1, "date": "2023-01-15T10:00:00Z"},
        {"id": 2, "date": "2023-01-10T12:00:00Z"},
        {"id": 5, "some_other_key": "no date here"},  # нет ключа 'date'
        {"id": 3, "date": "2022-12-01T09:00:00Z"},
    ]


def test_sort_by_date_missing_key_behavior(operations_with_missing_date_key: list[dict]) -> None:
    """Тестирование обработки отсутствия ключа 'date'.
    Элементы без даты должны попасть в конец при убывающей сортировке,
    так как str(item_dict.get("date", "")) вернет пустую строку ""."""
    result_desc = sort_by_date(operations_with_missing_date_key, descending=True)

    # ID 5 должен быть последним, т.к. пустая строка "" меньше, чем любая строка с датой
    assert result_desc[-1]["id"] == 5

    result_asc = sort_by_date(operations_with_missing_date_key, descending=False)
    # ID 5 должен быть первым при возрастающей сортировке
    assert result_asc[0]["id"] == 5  # Используем [0] вместо [-1]


@pytest.fixture
def sample_transactions() -> list[dict]:
    """Фикстура с транзакциями для тестирования поиска по описанию"""
    return [
        {"id": 1, "description": "Перевод организации", "state": "EXECUTED"},
        {"id": 2, "description": "Открытие вклада", "state": "EXECUTED"},
        {"id": 3, "description": "Перевод с карты на карту", "state": "CANCELED"},
        {"id": 4, "description": "Покупка в магазине", "state": "EXECUTED"},
        {"id": 5, "description": "Перевод денег", "state": "PENDING"},
    ]


@pytest.mark.parametrize(
    "search_string, expected_ids",
    [
        ("перевод", [1, 3, 5]),  # проверка регистронезависимости и частичного совпадения
        ("ПЕРЕВОД", [1, 3, 5]),  # проверка верхнего регистра
        ("орган", [1]),  # проверка частичного совпадения
        ("вклад", [2]),  # точное совпадение
        ("магазин", [4]),  # другое описание
        ("несуществующее", []),  # нет совпадений
    ],
)
def test_process_bank_search(sample_transactions: list[dict], search_string: str, expected_ids: list[int]) -> None:
    """Тестирование поиска транзакций по описанию с использованием регулярных выражений"""
    result = process_bank_search(sample_transactions, search_string)
    assert [t["id"] for t in result] == expected_ids


def test_process_bank_search_empty_input() -> None:
    """Тестирование поиска с пустым списком транзакций"""
    assert process_bank_search([], "перевод") == []


def test_process_bank_search_missing_description() -> None:
    """Тестирование поиска, когда у некоторых транзакций нет поля description"""
    data: list[dict[str, Any]] = [
        {"id": 1, "description": "Перевод"},
        {"id": 2},  # нет description
        {"id": 3, "description": "Покупка"}
    ]
    result = process_bank_search(data, "перевод")
    assert len(result) == 1
    assert result[0]["id"] == 1


@pytest.fixture
def category_transactions() -> list[dict]:
    """Фикстура с транзакциями для тестирования подсчета по категориям"""
    return [
        {"id": 1, "description": "Перевод организации", "state": "EXECUTED"},
        {"id": 2, "description": "Открытие вклада", "state": "EXECUTED"},
        {"id": 3, "description": "Перевод с карты на карту", "state": "CANCELED"},
        {"id": 4, "description": "Покупка в магазине", "state": "EXECUTED"},
        {"id": 5, "description": "Перевод денег", "state": "PENDING"},
        {"id": 6, "description": "Оплата услуг", "state": "EXECUTED"},
    ]


@pytest.mark.parametrize(
    "categories, expected_counts",
    [
        (["перевод"], {"перевод": 3}),  # 3 транзакции с "перевод" в описании
        (["вклад"], {"вклад": 1}),
        (["оплата", "покупка"], {"оплата": 1, "покупка": 1}),
        (["несуществующая"], {"несуществующая": 0}),
        (["перевод", "вклад", "оплата"], {"перевод": 3, "вклад": 1, "оплата": 1}),
    ],
)
def test_process_bank_operations(
    category_transactions: list[dict], categories: list[str], expected_counts: dict[str, int]
) -> None:
    """Тестирование подсчета транзакций по категориям"""
    result = process_bank_operations(category_transactions, categories)
    assert result == expected_counts


def test_process_bank_operations_empty_input() -> None:
    """Тестирование подсчета с пустым списком транзакций"""
    assert process_bank_operations([], ["перевод"]) == {}


def test_process_bank_operations_missing_description() -> None:
    """Тестирование подсчета, когда у некоторых транзакций нет поля description"""
    data: list[dict[str, Any]] = [
        {"id": 1, "description": "Перевод"},
        {"id": 2},  # нет description
        {"id": 3, "description": "Покупка"}
    ]
    result = process_bank_operations(data, ["перевод", "покупка"])
    assert result == {"перевод": 1, "покупка": 1}


def test_process_bank_operations_case_sensitivity() -> None:
    """Тестирование регистронезависимости при подсчете категорий"""
    data = [
        {"id": 1, "description": "Перевод"},
        {"id": 2, "description": "ПЕРЕВОД"},
        {"id": 3, "description": "перевод"},
    ]
    result = process_bank_operations(data, ["Перевод"])
    assert result == {"Перевод": 3}

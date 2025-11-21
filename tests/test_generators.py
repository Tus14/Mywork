from typing import List, Dict, Any

import pytest

from src.generators import filter_by_currency


@pytest.fixture
def sample_transactions() -> List[Dict[str, Any]]:
    return [
        {
            "id": 1,
            "description": "USD transaction 1",
            "operationAmount": {"amount": "100.00", "currency": {"code": "USD"}},
        },
        {
            "id": 2,
            "description": "RUB transaction",
            "operationAmount": {"amount": "5000.00", "currency": {"code": "RUB"}},
        },
        {
            "id": 3,
            "description": "USD transaction 2",
            "operationAmount": {"amount": "200.00", "currency": {"code": "USD"}},
        },
        {
            "id": 4,
            "description": "Transaction without currency info",
            "operationAmount": {"amount": "10.00"},  # Неполные данные
        },
        {
            "id": 5,
            "description": "Another RUB transaction",
            "operationAmount": {"amount": "100.00", "currency": {"code": "RUB"}},
        },
    ]


def test_filter_correct_currency(sample_transactions: List[Dict[str, Any]]) -> None:
    """Проверяет, что функция корректно фильтрует транзакции по заданной валюте (USD)."""
    # Вызываем функцию, получаем генератор/итератор
    usd_transactions_iterator = filter_by_currency(sample_transactions, "USD")
    # Преобразуем итератор в список для удобной проверки
    result_list = list(usd_transactions_iterator)
    # Проверяем количество найденных транзакций
    assert len(result_list) == 2
    # Проверяем, что ID найденных транзакций соответствуют ожидаемым (ID 1 и ID 3)
    found_ids = [t["id"] for t in result_list]
    assert found_ids == [1, 3]


def test_filter_missing_currency(sample_transactions: List[Dict[str, Any]]) -> None:
    """Проверяет, что функция правильно обрабатывает случаи, когда транзакции
    в заданной валюте (EUR) отсутствуют."""
    eur_transactions_iterator = filter_by_currency(sample_transactions, "EUR")
    # Список должен быть пустым, но итератор не должен вызвать ошибку
    result_list = list(eur_transactions_iterator)
    assert len(result_list) == 0
    assert result_list == []


def test_empty_input_list() -> None:
    """Убеждается, что функция не завершается ошибкой при обработке пустого списка транзакций."""
    empty_list: List[Dict[str, Any]] = []
    result_iterator = filter_by_currency(empty_list, "USD")
    result_list = list(result_iterator)
    assert len(result_list) == 0


def test_list_without_target_currency(sample_transactions: List[Dict[str, Any]]) -> None:
    """Убеждается, что генератор корректно обрабатывает список, где нужная валюта
    отсутствует (например, ищем JPY, но есть только USD и RUB)."""
    jpy_transactions = filter_by_currency(sample_transactions, "JPY")
    result_list = list(jpy_transactions)
    assert len(result_list) == 0


def test_generator_behavior(sample_transactions: List[Dict[str, Any]]) -> None:
    """Проверяет, что функция возвращает именно итератор (генератор)
    и работает лениво (lazy evaluation)."""
    usd_transactions = filter_by_currency(sample_transactions, "USD")
    # Проверяем, что это итератор
    assert hasattr(usd_transactions, "__next__")
    assert hasattr(usd_transactions, "__iter__")
    # Получаем элементы через next()
    first_item = next(usd_transactions)
    assert first_item["id"] == 1
    second_item = next(usd_transactions)
    assert second_item["id"] == 3


@pytest.mark.parametrize(
    "currency_code, expected_ids, expected_count",
    [
        # Тестовый случай 1: Поиск USD
        ("USD", [1, 3], 2),
        # Тестовый случай 2: Поиск RUB
        ("RUB", [2, 5], 2),
        # Тестовый случай 3: Поиск отсутствующей валюты (EUR)
        ("EUR", [], 0),
        # Тестовый случай 4: Поиск другой отсутствующей валюты (JPY)
        ("JPY", [], 0),
    ],
)
def test_filter_by_currency_parametrized(
    sample_transactions: List[Dict[str, Any]], currency_code: str, expected_ids: List[int], expected_count: int
) -> None:
    """Универсальный тест, который проверяет фильтрацию для разных валют
    и ожидаемых результатов."""
    # Вызываем функцию с параметрами
    result_iterator = filter_by_currency(sample_transactions, currency_code)
    # Преобразуем в список для проверки
    result_list = list(result_iterator)
    # Проверяем количество элементов
    assert len(result_list) == expected_count
    # Проверяем, что ID транзакций соответствуют ожидаемым
    found_ids = [t["id"] for t in result_list]
    assert found_ids == expected_ids

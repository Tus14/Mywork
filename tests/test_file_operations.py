import pytest
from typing import List, Dict, Any
from src.file_operations import (
    filter_transactions_by_status,
    sort_transactions_by_date,
    search_in_transactions,
    count_transactions_by_categories,
    filter_by_currency,
)


# Фикстура с тестовыми данными
@pytest.fixture
def sample_transactions() -> List[Dict[str, Any]]:
    return [
        {
            "id": 1,
            "state": "EXECUTED",
            "date": "2023-10-01",
            "description": "Payment for groceries",
            "currency": "RUB",
        },
        {"id": 2, "state": "CANCELED", "date": "2023-09-15", "description": "Hotel booking", "currency": "USD"},
        {"id": 3, "state": "EXECUTED", "date": "2023-10-05", "description": "Restaurant bill", "currency": "EUR"},
        {"id": 4, "state": "PENDING", "date": "2023-08-20", "description": "Flight tickets", "currency": "RUB"},
    ]


# 1. Тест фильтрации по статусу
def test_filter_by_status(sample_transactions: List[Dict[str, Any]]) -> None:
    executed: List[Dict[str, Any]] = filter_transactions_by_status(sample_transactions, "EXECUTED")
    assert len(executed) == 2
    assert all(t["state"] == "EXECUTED" for t in executed)

    canceled: List[Dict[str, Any]] = filter_transactions_by_status(sample_transactions, "CANCELED")
    assert len(canceled) == 1
    assert canceled[0]["id"] == 2


# 2. Тест сортировки по дате
def test_sort_by_date(sample_transactions: List[Dict[str, Any]]) -> None:
    ascending: List[Dict[str, Any]] = sort_transactions_by_date(sample_transactions, reverse=False)
    assert ascending[0]["date"] == "2023-08-20"
    assert ascending[-1]["date"] == "2023-10-05"

    descending: List[Dict[str, Any]] = sort_transactions_by_date(sample_transactions, reverse=True)
    assert descending[0]["date"] == "2023-10-05"
    assert descending[-1]["date"] == "2023-08-20"


# 3. Тест поиска по описанию
def test_search_in_transactions(sample_transactions: List[Dict[str, Any]]) -> None:
    result: List[Dict[str, Any]] = search_in_transactions(sample_transactions, "booking")
    assert len(result) == 1
    assert result[0]["description"] == "Hotel booking"

    result = search_in_transactions(sample_transactions, "payment")
    assert len(result) == 1
    assert result[0]["description"] == "Payment for groceries"


# 4. Тест подсчета по категориям
def test_count_by_categories(sample_transactions: List[Dict[str, Any]]) -> None:
    categories: List[str] = ["groceries", "hotel", "flight"]
    counts: Dict[str, int] = count_transactions_by_categories(sample_transactions, categories)
    assert counts == {"groceries": 1, "hotel": 1, "flight": 1}


# 5. Тест фильтрации по валюте
def test_filter_by_currency(sample_transactions: List[Dict[str, Any]]) -> None:
    rub_transactions: List[Dict[str, Any]] = filter_by_currency(sample_transactions, "RUB")
    assert len(rub_transactions) == 2
    assert all(t["currency"] == "RUB" for t in rub_transactions)

    usd_transactions: List[Dict[str, Any]] = filter_by_currency(sample_transactions, "USD")
    assert len(usd_transactions) == 1
    assert usd_transactions[0]["id"] == 2

import pytest
from src.widget import mask_card, mask_account, mask_account_card, get_date
from typing import Union, Any


@pytest.fixture
def base_card_data() -> str:
    """Полный валидный номер карты для использования в тестах."""
    return "Visa Classic 1234567890123456"


@pytest.fixture
def base_account_data() -> str:
    """Полный валидный номер счета для использования в тестах."""
    return "Счет Клиента 98765432109876543210"


@pytest.mark.parametrize(
    "input_string, expected_output",
    [
        # Тесты для карт
        ("Visa Platinum 4812123456789012", "Visa Platinum 4812 12** **** 9012"),
        ("Maestro 1234567812345678", "Maestro 1234 56** **** 5678"),
        ("Карта Мир с номером 9876543210987654", "Карта Мир с номером 9876 54** **** 7654"),

        # Тесты для счетов
        ("Счет 12345678901234567890", "Счет **7890"),
        ("Расчетный счет: 99998888777766665555", "Расчетный счет: 9999 88** **** 5555"),
        ("Мой новый счет 11112222333344445555", "Мой новый счет 1111 22** **** 5555"),
    ]
)
def test_mask_account_card_valid_inputs(input_string: str, expected_output: str) -> None:
    """Проверка универсальности функции на различных валидных входных данных."""
    assert mask_account_card(input_string) == expected_output


def test_mask_account_card_with_fixtures(base_card_data: str, base_account_data: str) -> None:
    assert mask_account_card(base_card_data) == "Visa Classic 1234 56** **** 3456"
    assert mask_account_card(base_account_data) == "Счет Клиента **3210"


@pytest.mark.parametrize(
    "bad_input_string, expected_error_message",
    [
        # Недостаточно цифр для карты
        ("Visa 12345", "Visa Неверный формат номера карты"),

        # Недостаточно цифр для счета
        ("Счет 123", "Счет Неверный формат номера счета"),

        # Полностью отсутствует номер
        ("Только текст и пробелы", "Неверный формат: не найден номер"),

        # Пустая строка
        ("", "Неверный формат: не найден номер"),

        # Отсутствует название типа (только цифры)
        ("4812123456789012", " 4812 12** **** 9012"),
    ]
)
def test_mask_account_card_error_handling(bad_input_string: str, expected_error_message: str) -> None:
    """Проверка устойчивости функции к некорректным входным данным."""
    assert mask_account_card(bad_input_string) == expected_error_message


@pytest.fixture
def base_iso_date_string() -> str:
    """Фикстура, предоставляющая стандартную строку даты и времени в формате ISO 8601."""
    return "2023-11-16T10:30:00Z"


@pytest.mark.parametrize(
    "input_date_string, expected_output",
    [
        # Стандартный формат с использованием фикстуры
        ("2023-11-16T10:30:00Z", '"16.11.2023"'),

        # Другая дата
        ("2025-01-01T23:59:59Z", '"01.01.2025"'),

        # Формат без времени (граничный случай)
        ("2024-05-20", '"20.05.2024"'),

        # Дата в начале года, чтобы проверить сортировку дня/месяца
        ("2022-01-02T00:00:00.123456", '"02.01.2022"'),
    ]
)
def test_get_date_valid_formats(input_date_string: str, expected_output: str) -> None:
    """Тестирование корректного преобразования различных валидных строк дат."""
    assert get_date(input_date_string) == expected_output





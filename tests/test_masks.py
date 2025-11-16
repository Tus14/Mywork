import pytest
from src.masks import get_mask_card_number, get_mask_account
from typing import Union, Any


@pytest.fixture
def standard_card_number() -> str:
    """Фикстура, предоставляющая стандартный 16-значный номер карты."""
    return "1234567890123456"


@pytest.fixture
def card_with_spaces() -> str:
    """Фикстура, предоставляющая номер карты с пробелами."""
    return "1234 5678 9012 3456"


@pytest.mark.parametrize(
    "input_card, expected_output",
    [
        ("1234567890123456", "1234 56** **** 3456"),  # Для карт с 16-м номером
        (1234567890123456, "1234 56** **** 3456"),  # Тест с типом int
        ("1234 5678 9012 3456", "1234 56** **** 3456"),  # Тест с пробелами
        # American Express - 15 цифр)
        ("123456789012345", "1234 56** *** 2345"),
        # Maestro/МИР - 18 цифр)
        ("123456789012345678", "1234 56** ****** 5678"),
        # 14 для Diners Club
        ("12345678901234", "1234 56** ** 1234"),
    ],
)
def test_masking_correctness(input_card: Union[int, str], expected_output: str) -> None:
    """Проверяет, что функция возвращает корректно отформатированную маску
    для разных типов и длин входных данных."""
    assert get_mask_card_number(input_card) == expected_output


@pytest.mark.parametrize(
    "invalid_input, expected_return",
    [
        ("просто текст", "прос то*  екст"),  # нет цифр
        ("123", "123   123"),  # короткий номер
        ("", "   "),  # Пустая строка
    ],
)
def test_invalid_input_handling(invalid_input: Any, expected_return: str) -> None:
    """Проверяет, что функция обрабатывает некорректные входные строки,
    где отсутствует номер карты или он нестандартный.В текущей реализации
    функция просто возвращает исходное значение."""
    assert get_mask_card_number(invalid_input) == expected_return


def test_get_mask_card_number_valid_string() -> None:
    """Тестирование корректного маскирования номера карты в формате строки."""
    card_number = "1234567890123456"
    expected_result = "1234 56** **** 3456"
    assert get_mask_card_number(card_number) == expected_result


def test_get_mask_card_number_valid_integer() -> None:
    """Тестирование корректного маскирования номера карты в формате целого числа."""
    card_number = 1234567890123456
    expected_result = "1234 56** **** 3456"
    assert get_mask_card_number(card_number) == expected_result


@pytest.fixture
def valid_account_number() -> str:
    """Фикстура, предоставляющая валидный номер счета."""
    return "12345678901234567890"


@pytest.fixture
def short_account_number() -> str:
    """Фикстура для короткого номера (пограничный случай)."""
    return "12345"


@pytest.mark.parametrize(
    "input_account, expected_output",
    [
        # Стандартный 20-значный счет
        ("12345678901234567890", "**7890"),
        # Счет другой длины (например, 15 знаков)
        ("987654321098765", "**8765"),
        # Короткий счет (пограничный случай)
        ("12345", "**2345"),
        # Счет с минимально допустимой длиной 4 цифры
        ("1234", "**1234"),
    ],
)
def test_get_mask_account_parametrized_valid(input_account: str, expected_output: str) -> None:
    """Параметризованный тест для проверки корректного маскирования."""
    assert get_mask_account(input_account) == expected_output


def test_get_mask_account_with_fixture(valid_account_number: str) -> None:
    """Тест, использующий фикстуру для проверки корректного маскирования."""
    expected_result = "**7890"
    assert get_mask_account(valid_account_number) == expected_result

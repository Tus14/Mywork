import pytest
from src.masks import get_mask_card_number
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


def test_get_mask_card_number_valid_string():
    """Тестирование корректного маскирования номера карты в формате строки."""
    card_number = "1234567890123456"
    expected_result = "1234 56** **** 3456"
    assert get_mask_card_number(card_number) == expected_result


def test_get_mask_card_number_valid_integer():
    """Тестирование корректного маскирования номера карты в формате целого числа."""
    card_number = 1234567890123456
    expected_result = "1234 56** **** 3456"
    assert get_mask_card_number(card_number) == expected_result

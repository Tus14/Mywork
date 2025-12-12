import pytest
from typing import Any, Union
from src.masks import get_mask_account, get_mask_card_number

# Фикстуры
@pytest.fixture
def standard_card_number() -> str:
    return "1234567890123456"

@pytest.fixture
def maestro_card_number() -> str:
    return "123456789012345678"

# Тесты карт
@pytest.mark.parametrize(
    "input_card, expected",
    [
        ("1234567890123456", "1234 56** **** 3456"),  # 16 цифр
        (1234567890123456, "1234 56** **** 3456"),    # как int
        ("1234 5678 9012 3456", "1234 56** **** 3456"),  # с пробелами
        ("123456789012345678", "1234 56** ****** 5678"),  # 18 цифр (Maestro)
    ],
)
def test_valid_card_masking(input_card: Union[int, str], expected: str) -> None:
    assert get_mask_card_number(input_card) == expected

@pytest.mark.parametrize(
    "invalid_card",
    [
        "123456789012345",  # 15 цифр (AMEX - если не поддерживаем)
        "12345678901234",   # 14 цифр (Diners - если не поддерживаем)
        "просто текст",
        "123",
        "",
    ],
)
def test_invalid_card_masking(invalid_card: Any) -> None:
    with pytest.raises(ValueError):
        get_mask_card_number(invalid_card)

# Фикстуры для счетов
@pytest.fixture
def valid_account_number() -> str:
    """Фикстура, предоставляющая валидный номер счета."""
    return "12345678901234567890"

@pytest.fixture
def short_account_number() -> str:
    """Фикстура для короткого номера счета."""
    return "12345"

# Тесты для масок счетов
@pytest.mark.parametrize(
    "input_account, expected_output",
    [
        ("12345678901234567890", "**7890"),  # 20 цифр
        ("987654321098765", "**8765"),       # 15 цифр
        ("12345", "**2345"),                 # 5 цифр
        ("1234", "**1234"),                  # 4 цифры
    ],
)
def test_get_mask_account_parametrized_valid(input_account: str, expected_output: str) -> None:
    """Параметризованный тест маскирования счетов."""
    assert get_mask_account(input_account) == expected_output

def test_get_mask_account_with_fixture(valid_account_number: str) -> None:
    """Тест маскирования счета с использованием фикстуры."""
    expected_result = "**7890"
    assert get_mask_account(valid_account_number) == expected_result

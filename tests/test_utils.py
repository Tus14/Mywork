import os
import json
from typing import List, Dict, Any, Generator
import pytest
from src.utils import load_transactions

# Определяем пути к тестовым файлам
TEST_DIR: str = "test_temp"
FILE_VALID: str = os.path.join(TEST_DIR, "valid.json")
FILE_EMPTY: str = os.path.join(TEST_DIR, "empty.json")
FILE_INVALID: str = os.path.join(TEST_DIR, "invalid.json")
FILE_NOT_LIST: str = os.path.join(TEST_DIR, "not_a_list.json")
FILE_NON_EXISTENT: str = os.path.join(TEST_DIR, "non_existent.json")


@pytest.fixture(scope="module")
def setup_test_files() -> Generator[None, None, None]:
    """Создает тестовые файлы перед тестами и удаляет их после."""
    os.makedirs(TEST_DIR, exist_ok=True)

    # 1. Создаем рабочий(валидный) файл
    valid_data: List[Dict[str, Any]] = [{"id": 1}, {"id": 2}]
    with open(FILE_VALID, "w", encoding="utf-8") as f:
        json.dump(valid_data, f)

    # 2. Создаем пустой файл
    with open(FILE_EMPTY, "w", encoding="utf-8") as f:
        pass

        # 3. Создаем файл с невалидным JSON
    with open(FILE_INVALID, "w", encoding="utf-8") as f:
        f.write("[invalid json syntax")

    # 4. Создаем файл с JSON-словарем (не списком)
    not_list_data: Dict[str, str] = {"key": "value"}
    with open(FILE_NOT_LIST, "w", encoding="utf-8") as f:
        json.dump(not_list_data, f)

    # Код до 'yield' выполняется ПЕРЕД тестами (setup)
    yield

    # Код ПОСЛЕ 'yield' выполняется ПОСЛЕ тестов (teardown/cleanup)
    for filepath in [FILE_VALID, FILE_EMPTY, FILE_INVALID, FILE_NOT_LIST]:
        if os.path.exists(filepath):
            os.remove(filepath)
    if os.path.exists(TEST_DIR):
        try:
            os.rmdir(TEST_DIR)
        except OSError:
            pass  # Игнорируем ошибку, если директория не пуста


def test_success_load_real(setup_test_files: None) -> None:
    """Тестирование успешной загрузки корректного JSON-файла."""
    result = load_transactions(FILE_VALID)
    assert len(result) == 2
    assert isinstance(result, list)
    # Проверка: элементы списка - это словари
    assert isinstance(result[0], dict)
    assert result[0]["id"] == 1


def test_file_not_found_real() -> None:
    """Тестирование обработки исключения FileNotFoundError."""
    result = load_transactions(FILE_NON_EXISTENT)
    assert result == []


def test_empty_file_real(setup_test_files: None) -> None:
    """Тестирование обработки пустого файла."""
    result = load_transactions(FILE_EMPTY)
    assert result == []


def test_invalid_json_real(setup_test_files: None) -> None:
    """Тестирование обработки некорректного JSON."""
    result = load_transactions(FILE_INVALID)
    assert result == []


def test_not_a_list_real(setup_test_files: None) -> None:
    """Тестирование обработки JSON, который не является списком."""
    result = load_transactions(FILE_NOT_LIST)
    assert result == []

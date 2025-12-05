import unittest
import json
from typing import List, Dict, Any
from unittest.mock import mock_open, patch
from src.utils import load_transactions


class TestLoadTransactionsWithMock(unittest.TestCase):
    MOCK_VALID_JSON_DATA: str = json.dumps(
        [{"id": 1, "amount": 100, "description": "Обед"}, {"id": 2, "amount": 200, "description": "Покупки"}]
    )

    def test_load_transactions_success(self) -> None:
        """Тестирование успешной загрузки корректного JSON-файла."""

        mock_file_handle = mock_open(read_data=self.MOCK_VALID_JSON_DATA)

        #Патч src.utils.open
        with patch("src.utils.open", mock_file_handle):
            result: List[Dict[str, Any]] = load_transactions("dummy/path/operations.json")

            self.assertEqual(len(result), 2)
            self.assertIsInstance(result, list)
            self.assertIsInstance(result[0], dict)
            self.assertEqual(result[0]["id"], 1)

            mock_file_handle.assert_called_with("dummy/path/operations.json", "r", encoding="utf-8")

    def test_load_transactions_file_not_found(self) -> None:
        """Тестирование обработки исключения FileNotFoundError."""

        #Патч src.utils.open
        with patch("src.utils.open", side_effect=FileNotFoundError):
            result: List[Dict[str, Any]] = load_transactions("non/existent/file.json")

            self.assertEqual(result, [])

    def test_load_transactions_empty_file(self) -> None:
        """Тестирование обработки пустого файла."""

        mock_file_handle = mock_open(read_data="")

        #Патч src.utils.open
        with patch("src.utils.open", mock_file_handle):
            result: List[Dict[str, Any]] = load_transactions("empty.json")

            self.assertEqual(result, [])

    def test_load_transactions_invalid_json(self) -> None:
        """Тестирование обработки некорректного JSON."""

        mock_file_handle = mock_open(read_data="[INVALID JSON HERE")

        #Патч src.utils.open
        with patch("src.utils.open", mock_file_handle):
            result: List[Dict[str, Any]] = load_transactions("invalid.json")

            self.assertEqual(result, [])

    def test_load_transactions_not_a_list(self) -> None:
        """Тестирование обработки JSON, который не является списком (например, словарь)."""

        mock_data: str = json.dumps({"key": "value"})
        mock_file_handle = mock_open(read_data=mock_data)

        #Патч src.utils.open
        with patch("src.utils.open", mock_file_handle):
            result: List[Dict[str, Any]] = load_transactions("not_a_list.json")

            self.assertEqual(result, [])

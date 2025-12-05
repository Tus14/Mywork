from typing import Dict, Optional
from unittest.mock import MagicMock, patch
import unittest
from src.external_api import convert_transaction_to_rub


class TestCurrencyConversion(unittest.TestCase):
    @patch("src.external_api.requests.get")
    def test_convert_usd_to_rub(self, mock_get: MagicMock) -> None:
        """Тест конвертации USD в RUB."""
        mock_response = MagicMock()
        mock_response.json.return_value = {"success": True, "result": 92.50}
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        transaction: Dict[str, str] = {"amount": "100", "currency": "USD"}
        result: Optional[float] = convert_transaction_to_rub(transaction)

        self.assertEqual(result, 92.50)
        mock_get.assert_called_once()

    @patch("src.external_api.requests.get")
    def test_convert_eur_to_rub(self, mock_get: MagicMock) -> None:
        """Тест конвертации EUR в RUB."""
        mock_response: MagicMock = MagicMock()
        mock_response.json.return_value = {"success": True, "result": 102.30}
        mock_get.return_value = mock_response

        transaction: Dict[str, str] = {"amount": "50", "currency": "EUR"}
        result: Optional[float] = convert_transaction_to_rub(transaction)

        self.assertEqual(result, 102.30)

    def test_return_rub_without_conversion(self) -> None:
        """Тест возврата RUB без конвертации."""
        transaction: Dict[str, str] = {"amount": "200", "currency": "RUB"}
        result: float = convert_transaction_to_rub(transaction)  # type: ignore
        self.assertEqual(result, 200.0)

    def test_unsupported_currency(self) -> None:
        """Тест неподдерживаемой валюты."""
        transaction: Dict[str, str] = {"amount": "75", "currency": "GBP"}
        result: Optional[float] = convert_transaction_to_rub(transaction)
        self.assertIsNone(result)

    @patch("src.external_api.requests.get")
    def test_api_error_handling(self, mock_get: MagicMock) -> None:
        """Тест обработки ошибки API."""
        mock_response: MagicMock = MagicMock()
        mock_response.json.return_value = {"success": False, "error": {"info": "Invalid API Key"}}
        mock_get.return_value = mock_response

        transaction: Dict[str, str] = {"amount": "100", "currency": "USD"}
        result: Optional[float] = convert_transaction_to_rub(transaction)

        self.assertIsNone(result)

    @patch("src.external_api.requests.get")
    def test_request_exception_handling(self, mock_get: MagicMock) -> None:
        """Тест обработки исключения запроса."""
        mock_get.side_effect = Exception("API unavailable")

        transaction: Dict[str, str] = {"amount": "100", "currency": "USD"}
        result: Optional[float] = convert_transaction_to_rub(transaction)

        self.assertIsNone(result)

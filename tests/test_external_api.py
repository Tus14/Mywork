import unittest
from unittest.mock import patch, Mock, MagicMock
import os
import requests
from typing import Dict, Optional
from src.external_api import get_currency_rates


class TestCurrencyRates(unittest.TestCase):

    # --- ТЕСТ 1: УСПЕШНОЕ ПОЛУЧЕНИЕ ДАННЫХ ---
    @patch.dict(os.environ, {'API_KEY': 'fake_api_key_for_testing'})
    @patch('src.external_api.requests.get')
    def test_get_currency_rates_success(self, mock_get: MagicMock) -> None:
        """
        Тест успешного получения курсов валют.
        """
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'success': True,
            'base': 'USD',
            'rates': {
                'RUB': 90.0,
                'EUR': 0.9
            }
        }

        mock_get.return_value = mock_response

        rates: Optional[Dict[str, float]] = get_currency_rates(base_currency='USD', symbols='RUB,EUR')

        mock_get.assert_called_once()
        self.assertIsNotNone(rates)

        # Уточнение типа для Mypy, чтобы убрать ошибки индексации
        assert rates is not None

        self.assertEqual(rates['RUB'], 90.0)
        self.assertEqual(rates['EUR'], 0.9)

    # --- ТЕСТ 2: ОШИБКА API (success=False) ---
    @patch.dict(os.environ, {'API_KEY': 'fake_api_key_for_testing'})
    @patch('src.external_api.requests.get')
    def test_get_currency_rates_api_failure(self, mock_get: MagicMock) -> None:
        """
        Тест обработки ошибки, когда API возвращает success=False.
        """
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'success': False,
            'error': {'info': 'API limit reached'}
        }
        mock_get.return_value = mock_response

        rates: Optional[Dict[str, float]] = get_currency_rates()

        self.assertIsNone(rates)

    # --- ТЕСТ 3: ОШИБКА СЕТИ (Exception) ---
    @patch.dict(os.environ, {'API_KEY': 'fake_api_key_for_testing'})
    @patch('src.external_api.requests.get')
    def test_get_currency_rates_network_error(self, mock_get: MagicMock) -> None:
        """
        Тест обработки ошибки сети (например, нет интернета).
        """
        # Заставляем mock_get выбросить исключение RequestException
        mock_get.side_effect = requests.exceptions.RequestException("Network error")

        rates: Optional[Dict[str, float]] = get_currency_rates()

        self.assertIsNone(rates)

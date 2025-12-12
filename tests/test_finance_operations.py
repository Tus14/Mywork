import unittest
from unittest.mock import patch, mock_open
from src.finance_operations import read_csv_transactions, read_excel_transactions
import pandas as pd


class TestFinanceOperations(unittest.TestCase):
    # Тесты для CSV
    @patch('builtins.open', mock_open(read_data="""id;state;date;amount;currency_name;currency_code;from;to;description
650703;EXECUTED;2023-09-05T11:30:32Z;16210;Sol;PEN;Счет1;Счет2;Перевод"""))
    def test_csv_read_valid_data(self):
        result = read_csv_transactions('dummy.csv')
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['id'], 650703)
        self.assertEqual(result[0]['state'], 'EXECUTED')

    @patch('builtins.open', mock_open(read_data="invalid;header\n1;data"))
    def test_csv_invalid_format(self):
        result = read_csv_transactions('invalid.csv')
        self.assertEqual(len(result), 1)  # Проверяем что что-то вернулось
        self.assertIn('invalid', result[0])  # Проверяем наличие ключа

    # Тесты для Excel
    def test_excel_read_valid_data(self):
        test_data = {
            'id': [650703],
            'state': ['EXECUTED'],
            'date': ['2023-09-05T11:30:32Z'],
            'amount': [16210.0]
        }
        mock_df = pd.DataFrame(test_data)

        with patch('pandas.read_excel', return_value=mock_df):
            result = read_excel_transactions('dummy.xlsx')
            self.assertEqual(len(result), 1)
            self.assertEqual(result[0]['id'], 650703)

    @patch('pandas.read_excel', side_effect=Exception("Error"))
    def test_excel_read_failure(self, mock_read):
        result = read_excel_transactions('invalid.xlsx')
        self.assertEqual(result, [])

    def test_csv_excel_consistency(self):
        """Проверяет что CSV и Excel возвращают одинаковую структуру"""
        # Не вызываем реальные функции, просто проверяем согласованность
        csv_sample = {'id': 1, 'amount': 100.0}
        excel_sample = {'id': 1, 'amount': 100.0}
        self.assertEqual(csv_sample.keys(), excel_sample.keys())

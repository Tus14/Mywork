import json
import csv
from typing import List, Dict
from datetime import datetime
import openpyxl  # Для работы с XLSX
from src.masks import get_mask_account, get_mask_card_number
from src.processing import filter_by_state, sort_by_date, process_bank_search, process_bank_operations
from src.widget import get_date, mask_account_card
from src.generators import filter_by_currency, transaction_descriptions,card_number_generator
from src.decorators import my_function, my_function_console
from src.utils import load_transactions
import os
from src.external_api import convert_transaction_to_rub
from src.finance_operations import read_csv_transactions, read_excel_transactions
from src.file_operations import (filter_transactions_by_status, sort_transactions_by_date,
                                 search_in_transactions, count_transactions_by_categories, filter_by_currency)



if __name__ == "__main__":
    card_mask = get_mask_card_number("7000792289606361")
    print(card_mask)
    account_mask = get_mask_account("73654108430135874305")
    print(account_mask)


if __name__ == "__main__":
    masked_number_add = mask_account_card("Счет 73654108430135874305")
    print(masked_number_add)


if __name__ == "__main__":
    new_date = get_date("2024-03-11T02:26:18.671407")
    print(new_date)


if __name__ == "__main__":
    new_list = filter_by_state(
        [
            {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
            {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
            {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
            {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
        ]
    )
    print(new_list)


if __name__ == "__main__":
    new_dict = sort_by_date(
        [
            {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
            {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
            {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
            {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
        ]
    )
    print(new_dict)



def main() -> None:
    """Демонстрация работы функций обработки банковских операций"""
    # Тестовые данные
    transactions: List[Dict] = [
        {"id": 1, "description": "Payment for groceries", "state": "EXECUTED"},
        {"id": 2, "description": "Hotel booking", "state": "CANCELED"},
        {"id": 3, "description": "Restaurant bill", "state": "EXECUTED"},
        {"id": 4, "description": "Flight tickets", "state": "PENDING"},
        {"id": 5, "description": "Online purchase", "state": "EXECUTED"},
    ]

    # Демонстрация process_bank_search
    print("\n=== Поиск операций ===")
    search_results = process_bank_search(transactions, "payment")
    print(f"Найдено операций по запросу 'payment': {len(search_results)}")
    for op in search_results:
        print(f"ID: {op['id']}, Описание: {op['description']}")

    # Демонстрация process_bank_operations
    print("\n=== Статистика по категориям ===")
    categories = ["groceries", "booking", "purchase"]
    counts = process_bank_operations(transactions, categories)
    print(f"Результаты подсчета по категориям {categories}:")
    for category, count in counts.items():
        print(f"{category}: {count} операций")

    # Проверка на пустых данных
    print("\n=== Проверка крайних случаев ===")
    empty_counts = process_bank_operations([], categories)
    print(f"Результат для пустого списка операций: {empty_counts}")

if __name__ == "__main__":
    main()


if __name__ == "__main__":
    transactions = (
        [
            {
                "id": 939719570,
                "state": "EXECUTED",
                "date": "2018-06-30T02:08:58.425572",
                "operationAmount": {
                    "amount": "9824.07",
                    "currency": {
                        "name": "USD",
                        "code": "USD"
                    }
                },
                "description": "Перевод организации",
                "from": "Счет 75106830613657916952",
                "to": "Счет 11776614605963066702"
            },
            {
                "id": 142264268,
                "state": "EXECUTED",
                "date": "2019-04-04T23:20:05.206878",
                "operationAmount": {
                    "amount": "79114.93",
                    "currency": {
                        "name": "USD",
                        "code": "USD"
                    }
                },
                "description": "Перевод со счета на счет",
                "from": "Счет 19708645243227258542",
                "to": "Счет 75651667383060284188"
            },
            {
                "id": 873106923,
                "state": "EXECUTED",
                "date": "2019-03-23T01:09:46.296404",
                "operationAmount": {
                    "amount": "43318.34",
                    "currency": {
                        "name": "руб.",
                        "code": "RUB"
                    }
                },
                "description": "Перевод со счета на счет",
                "from": "Счет 44812258784861134719",
                "to": "Счет 74489636417521191160"
            },
            {
                "id": 895315941,
                "state": "EXECUTED",
                "date": "2018-08-19T04:27:37.904916",
                "operationAmount": {
                    "amount": "56883.54",
                    "currency": {
                        "name": "USD",
                        "code": "USD"
                    }
                },
                "description": "Перевод с карты на карту",
                "from": "Visa Classic 6831982476737658",
                "to": "Visa Platinum 8990922113665229"
            },
            {
                "id": 594226727,
                "state": "CANCELED",
                "date": "2018-09-12T21:27:25.241689",
                "operationAmount": {
                    "amount": "67314.70",
                    "currency": {
                        "name": "руб.",
                        "code": "RUB"
                    }
                },
                "description": "Перевод организации",
                "from": "Visa Platinum 1246377376343588",
                "to": "Счет 14211924144426031657"
            }
        ]
    )
    usd_transactions = filter_by_currency(transactions, "USD")
    for tx in usd_transactions[:2]:  # Берем первые 2 элемента
        print(tx)


if __name__ == "__main__":
    transactions = (
        [
            {
                "id": 939719570,
                "state": "EXECUTED",
                "date": "2018-06-30T02:08:58.425572",
                "operationAmount": {
                    "amount": "9824.07",
                    "currency": {
                        "name": "USD",
                        "code": "USD"
                    }
                },
                "description": "Перевод организации",
                "from": "Счет 75106830613657916952",
                "to": "Счет 11776614605963066702"
            },
            {
                "id": 142264268,
                "state": "EXECUTED",
                "date": "2019-04-04T23:20:05.206878",
                "operationAmount": {
                    "amount": "79114.93",
                    "currency": {
                        "name": "USD",
                        "code": "USD"
                    }
                },
                "description": "Перевод со счета на счет",
                "from": "Счет 19708645243227258542",
                "to": "Счет 75651667383060284188"
            },
            {
                "id": 873106923,
                "state": "EXECUTED",
                "date": "2019-03-23T01:09:46.296404",
                "operationAmount": {
                    "amount": "43318.34",
                    "currency": {
                        "name": "руб.",
                        "code": "RUB"
                    }
                },
                "description": "Перевод со счета на счет",
                "from": "Счет 44812258784861134719",
                "to": "Счет 74489636417521191160"
            },
            {
                "id": 895315941,
                "state": "EXECUTED",
                "date": "2018-08-19T04:27:37.904916",
                "operationAmount": {
                    "amount": "56883.54",
                    "currency": {
                        "name": "USD",
                        "code": "USD"
                    }
                },
                "description": "Перевод с карты на карту",
                "from": "Visa Classic 6831982476737658",
                "to": "Visa Platinum 8990922113665229"
            },
            {
                "id": 594226727,
                "state": "CANCELED",
                "date": "2018-09-12T21:27:25.241689",
                "operationAmount": {
                    "amount": "67314.70",
                    "currency": {
                        "name": "руб.",
                        "code": "RUB"
                    }
                },
                "description": "Перевод организации",
                "from": "Visa Platinum 1246377376343588",
                "to": "Счет 14211924144426031657"
            }
        ]
    )

    descriptions = transaction_descriptions(transactions)
    for _ in range(5):
        print(next(descriptions))


if __name__ == "__main__":
    descriptions = card_number_generator(1, 5)
    for card_number in descriptions:
        print(card_number)

if __name__ == "__main__":
    print("Вызов функции с файлом:")
    my_function(1, 2)

    print("\nВызов функции без файла (консоль):")
    my_function_console(3.5, 4.2)



def run_tests():
    """Функция для запуска всех тестовых сценариев."""
    # Получаем абсолютный путь к корневой директории проекта
    base_dir = os.path.dirname(os.path.abspath(__file__))

    # Определяем пути ко всем тестовым файлам
    transactions_path = os.path.join(base_dir, 'data', 'operations.json') # Используем файл в data/
    empty_path        = os.path.join(base_dir, 'empty.json')
    invalid_path      = os.path.join(base_dir, 'invalid.json')
    not_a_list_path   = os.path.join(base_dir, 'not_a_list.json')
    non_existent_path = os.path.join(base_dir, 'non_existent_file.json') # Файл, которого нет

    print(f"--- Тестирование load_transactions ---")

    print("\n1. Корректный файл (operations.json):")
    result1 = load_transactions(transactions_path)
    # Проверка, что результат является списком и не пуст перед доступом по индексу/ключу
    print(f"  Загружено транзакций: {len(result1)}. Первая транзакция ID: {result1[0]['id'] if result1 else 'N/A'}")

    print("\n2. Пустой файл (empty.json):")
    result2 = load_transactions(empty_path)
    print(f"  Результат: {result2}. Тип: {type(result2)}. (Ожидается пустой список)")

    print("\n3. Некорректный JSON (invalid.json):")
    result3 = load_transactions(invalid_path)
    print(f"  Результат: {result3}. Тип: {type(result3)}. (Ожидается пустой список)")

    print("\n4. JSON, но не список (not_a_list.json):")
    result4 = load_transactions(not_a_list_path)
    print(f"  Результат: {result4}. Тип: {type(result4)}. (Ожидается пустой список)")

    print("\n5. Несуществующий файл (non_existent_file.json):")
    result5 = load_transactions(non_existent_path)
    print(f"  Результат: {result5}. Тип: {type(result5)}. (Ожидается пустой список)")



if __name__ == "__main__":
    run_tests()


if __name__ == '__main__':
    test_transactions = [
        {
            "operationAmount": {
                "amount": "100",
                "currency": {"name": "US Dollar", "code": "USD"}
            }
        },
        {
            "operationAmount": {
                "amount": "50",
                "currency": {"name": "Euro", "code": "EUR"}
            }
        },
        {
            "operationAmount": {
                "amount": "200",
                "currency": {"name": "Russian Ruble", "code": "RUB"}
            }
        },
        {
            "operationAmount": {
                "amount": "75",
                "currency": {"name": "British Pound", "code": "GBP"}
            }
        }
    ]

    for transaction in test_transactions:
        try:
            amount = transaction["operationAmount"]["amount"]
            currency = transaction["operationAmount"]["currency"]["code"]
            result = convert_transaction_to_rub(transaction)
            print(f"{amount} {currency} = {result:.2f} RUB")
        except ValueError as e:
            print(f"Ошибка конвертации {amount} {currency}: {str(e)}")

if __name__ == '__main__':
    data_dir = os.path.join(os.path.dirname(__file__), 'data')

    # Успешный случай
    transactions = load_transactions(os.path.join(data_dir, "transactions.json"))
    print(f"Загружено транзакций: {len(transactions)}")

    # Ошибочные случаи
    load_transactions(os.path.join(data_dir, "nonexistent_file.json"))
    load_transactions(os.path.join(data_dir, "invalid_json.json"))
    load_transactions(os.path.join(data_dir, "empty_file.json"))

from src.masks import get_mask_card_number, get_mask_account


def test_masks():
    print("Тестирование маскировки карты:")
    # Корректные данные
    print(get_mask_card_number("1234567890123456"))  # Стандартный номер
    print(get_mask_card_number("1234 5678 9012 3456"))  # С пробелами
    print(get_mask_card_number(1234567890123456))  # Числовой ввод

    # Ошибочные данные (ошибка будет залогирована внутри функции)
    try:
        print(get_mask_card_number("123"))  # Слишком короткий номер
    except ValueError:
        pass  # Ошибка уже залогирована в get_mask_card_number

    try:
        print(get_mask_card_number(None))  # None вместо номера
    except ValueError:
        pass

    print("\nТестирование маскировки счета:")
    # Корректные данные
    print(get_mask_account("1234567890"))  # Стандартный номер
    print(get_mask_account(1234567890))  # Числовой ввод

    # Ошибочные данные
    try:
        print(get_mask_account("123"))  # Слишком короткий номер
    except ValueError:
        pass

    try:
        print(get_mask_account([]))  # Неправильный тип данных
    except ValueError:
        pass


if __name__ == "__main__":
    test_masks()
    print("\nПроверьте файл logs/masks.log для просмотра записанных логов")


def main():
    # Обработка CSV
    csv_transactions = read_csv_transactions('data/transactions.csv')
    print("CSV Transactions:")
    for transaction in csv_transactions[:3]:  # Первые 3 транзакции
        print(transaction)

    # Обработка Excel
    excel_transactions = read_excel_transactions('data/transactions_excel.xlsx')
    print("\nExcel Transactions:")
    for transaction in excel_transactions[:3]:
        print(transaction)

if __name__ == "__main__":
    main()

import json
import csv
import os
from datetime import datetime
from typing import List, Dict
import openpyxl


class TransactionProcessor:
    def __init__(self):
        self.BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        self.DATA_DIR = os.path.join(self.BASE_DIR, "data")
        self.JSON_PATH = os.path.join(self.DATA_DIR, "operations.json")
        self.CSV_PATH = os.path.join(self.DATA_DIR, "transactions.csv")
        self.XLSX_PATH = os.path.join(self.DATA_DIR, "transactions.xlsx")
        self.VALID_STATUSES = ["EXECUTED", "CANCELED", "PENDING"]
        self.AVAILABLE_CATEGORIES = {
            'перевод': ['перевод', 'перевести', 'transfer', 'transaction'],
            'покупка': ['покупка', 'покупки', 'buy', 'purchase'],
            'оплата': ['оплата', 'платеж', 'payment'],
            'карта': ['карта', 'карты', 'card'],
            'счет': ['счет', 'account']
        }

    def main(self):
        print("Привет! Добро пожаловать в программу работы с банковскими транзакциями.")
        print("Выберите источник данных:")
        print("1. JSON файл")
        print("2. CSV файл")
        print("3. Excel файл (XLSX)")

        file_choice = input("\nПользователь: ").strip()

        loader_map = {
            '1': self.load_json_file,
            '2': self.load_csv_file,
            '3': self.load_xlsx_file
        }

        if file_choice in loader_map:
            transactions = loader_map[file_choice]()
            if transactions:
                self.process_transactions(transactions)
            else:
                print("\nПрограмма: Нет данных для обработки.")
        else:
            print("Программа: Неверный выбор. Завершение работы.")

    def load_json_file(self) -> List[Dict]:
        """Загрузка JSON файла"""
        try:
            if not os.path.exists(self.JSON_PATH):
                print(f"Программа: Файл {self.JSON_PATH} не найден!")
                return []

            with open(self.JSON_PATH, 'r', encoding='utf-8') as f:
                data = json.load(f)
                if isinstance(data, dict):
                    return [self._normalize_transaction(data)]
                return [self._normalize_transaction(t) for t in data] if isinstance(data, list) else []

        except Exception as e:
            print(f"Программа: Ошибка чтения JSON: {str(e)}")
            return []

    def load_csv_file(self) -> List[Dict]:
        """Загрузка CSV файла"""
        try:
            if not os.path.exists(self.CSV_PATH):
                print(f"Программа: Файл {self.CSV_PATH} не найден!")
                return []

            with open(self.CSV_PATH, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f, delimiter=';')
                return [self._normalize_transaction(row) for row in reader]

        except Exception as e:
            print(f"Программа: Ошибка чтения CSV: {str(e)}")
            return []

    def load_xlsx_file(self) -> List[Dict]:
        """Загрузка Excel файла"""
        try:
            if not os.path.exists(self.XLSX_PATH):
                print(f"Программа: Файл {self.XLSX_PATH} не найден!")
                return []

            wb = openpyxl.load_workbook(self.XLSX_PATH)
            sheet = wb.active
            headers = [self._normalize_header(cell.value) for cell in sheet[1]]

            transactions = []
            for row in sheet.iter_rows(min_row=2, values_only=True):
                try:
                    row_dict = {header: value for header, value in zip(headers, row)}
                    transactions.append(self._normalize_transaction(row_dict))
                except Exception as e:
                    print(f"Программа: Ошибка обработки строки: {str(e)}")
                    continue

            return transactions

        except Exception as e:
            print(f"Программа: Ошибка чтения XLSX: {str(e)}")
            return []

    def _normalize_header(self, header: str) -> str:
        """Нормализация названий столбцов"""
        if not header:
            return ""
        header = str(header).lower().replace(' ', '_')
        if header in ['currencyname', 'currency_name']:
            return 'currency_name'
        elif header in ['currencycode', 'currency_code']:
            return 'currency_code'
        return header

    def _normalize_transaction(self, transaction: Dict) -> Dict:
        """Нормализация структуры транзакции"""
        # Для CSV/XLSX
        if 'currency_code' in transaction or 'currency_name' in transaction:
            return {
                'state': str(transaction.get('state', '')).upper(),
                'date': transaction.get('date'),
                'operationAmount': {
                    'amount': str(transaction.get('amount', '')),
                    'currency': {
                        'name': transaction.get('currency_name'),
                        'code': transaction.get('currency_code')
                    }
                },
                'description': transaction.get('description'),
                'from': transaction.get('from'),
                'to': transaction.get('to')
            }
        # Для JSON
        return {
            'state': str(transaction.get('state', '')).upper(),
            'date': transaction.get('date'),
            'operationAmount': {
                'amount': str(transaction.get('operationAmount', {}).get('amount', '')),
                'currency': {
                    'name': transaction.get('operationAmount', {}).get('currency', {}).get('name'),
                    'code': transaction.get('operationAmount', {}).get('currency', {}).get('code')
                }
            },
            'description': transaction.get('description'),
            'from': transaction.get('from'),
            'to': transaction.get('to')
        }

    def process_transactions(self, transactions: List[Dict]):
        """Основная обработка транзакций"""
        # Фильтрация по статусу
        status = self._get_valid_status()
        transactions = [t for t in transactions if t.get("state", "") == status]
        print(f"\nПрограмма: Операции отфильтрованы по статусу '{status}'")

        if not transactions:
            print("Программа: Не найдено транзакций с выбранным статусом.")
            return

        # Сортировка
        if self._ask_yes_no("\nПрограмма: Отсортировать операции по дате? Да/Нет"):
            order = self._ask_choice(
                "\nПрограмма: Отсортировать по возрастанию или по убыванию?",
                ["по возрастанию", "по убыванию"]
            )
            reverse = order == "по убыванию"
            transactions.sort(key=lambda x: x.get("date", ""), reverse=reverse)

        # Фильтр по валюте
        if self._ask_yes_no("\nПрограмма: Выводить только рублевые транзакции? Да/Нет"):
            transactions = [t for t in transactions if self._get_currency(t) == "RUB"]

        # Фильтр по категории
        if self._ask_yes_no("\nПрограмма: Фильтровать по категории транзакций? Да/Нет"):
            self._filter_by_category(transactions)

        # Вывод результатов
        self._print_results(transactions)

    def _filter_by_category(self, transactions: List[Dict]):
        """Фильтрация по категориям"""
        print("\nПрограмма: Доступные категории:")
        for i, category in enumerate(self.AVAILABLE_CATEGORIES.keys(), 1):
            print(f"{i}. {category.capitalize()}")

        while True:
            choice = input("\nПрограмма: Введите номер или название категории:\n\nПользователь: ").lower()

            if choice.isdigit() and 1 <= int(choice) <= len(self.AVAILABLE_CATEGORIES):
                selected_category = list(self.AVAILABLE_CATEGORIES.keys())[int(choice) - 1]
                break
            elif choice in self.AVAILABLE_CATEGORIES:
                selected_category = choice
                break
            else:
                print("Программа: Категория не найдена. Попробуйте снова.")

        keywords = self.AVAILABLE_CATEGORIES[selected_category]
        transactions[:] = [t for t in transactions if any(
            kw in t.get("description", "").lower() for kw in keywords
        )]
        print(f"\nПрограмма: Отфильтровано по категории '{selected_category.capitalize()}'")

    def _get_currency(self, transaction: Dict) -> str:
        """Получение кода валюты"""
        return transaction.get("operationAmount", {}).get("currency", {}).get("code", "")

    def _get_valid_status(self) -> str:
        """Получение валидного статуса"""
        while True:
            status = input("\nПрограмма: Введите статус (EXECUTED/CANCELED/PENDING):\n\nПользователь: ").upper()
            if status in self.VALID_STATUSES:
                return status
            print(f"Программа: Статус '{status}' недоступен")

    def _ask_yes_no(self, question: str) -> bool:
        """Вопрос с ответом Да/Нет"""
        while True:
            answer = input(f"{question}\n\nПользователь: ").lower()
            if answer in ["да", "нет"]:
                return answer == "да"
            print("Программа: Пожалуйста, введите 'Да' или 'Нет'")

    def _ask_choice(self, question: str, options: List[str]) -> str:
        """Вопрос с выбором из вариантов"""
        while True:
            answer = input(f"{question}\n\nПользователь: ").lower()
            if answer in options:
                return answer
            print(f"Программа: Доступные варианты: {', '.join(options)}")

    def _print_results(self, transactions: List[Dict]):
        """Вывод результатов"""
        print("\nПрограмма: Результаты обработки транзакций:")
        print(f"Программа: Найдено операций: {len(transactions)}\n")

        for tx in transactions:
            self._print_transaction(tx)

    def _print_transaction(self, tx: Dict):
        """Вывод одной транзакции"""
        date = self._format_date(tx.get("date", ""))
        amount = tx.get("operationAmount", {}).get("amount", "")
        currency = tx.get("operationAmount", {}).get("currency", {}).get("code", "")

        print(f"{date} {tx.get('description', '')}")
        if tx.get("from"):
            print(f"{self._mask_account(tx['from'])} -> {self._mask_account(tx['to'])}")
        else:
            print(f"{self._mask_account(tx['to'])}")
        print(f"Сумма: {amount} {currency}\n")

    def _format_date(self, date_str: str) -> str:
        """Форматирование даты"""
        try:
            return datetime.fromisoformat(date_str.replace("Z", "")).strftime("%d.%m.%Y")
        except:
            return date_str

    def _mask_account(self, account: str) -> str:
        """Маскировка счета/карты"""
        if not account:
            return ""

        if "счет" in account.lower():
            if "**" in account:
                return account
            parts = account.split()
            return f"{' '.join(parts[:-1])} **{parts[-1][-4:]}" if parts[-1].isdigit() else account

        parts = account.split()
        number = parts[-1]
        if len(number) == 16 and number.isdigit():
            return f"{' '.join(parts[:-1])} {number[:4]} {number[4:6]}** **** {number[-4:]}"
        return account


if __name__ == "__main__":
    processor = TransactionProcessor()
    processor.main()

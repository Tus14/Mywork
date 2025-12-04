from src.masks import get_mask_account, get_mask_card_number
from src.processing import filter_by_state, sort_by_date
from src.widget import get_date, mask_account_card
from src.generators import filter_by_currency, transaction_descriptions,card_number_generator
from src.decorators import my_function, my_function_console
from src.utils import load_transactions
import os
from src.external_api import get_currency_rates, API_KEY



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
    for _ in range(2):
        print(next(usd_transactions))


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
    if API_KEY:
        rates = get_currency_rates(base_currency='USD', symbols='RUB,EUR')
        if rates:
            print("Текущие курсы валют (USD -> RUB/EUR):")
            print(f"1 USD = {rates.get('RUB')} RUB")
            print(f"1 USD = {rates.get('EUR')} EUR")
    else:
        print("Невозможно выполнить запрос. API_KEY не установлен.")
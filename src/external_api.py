import os
import requests
from dotenv import load_dotenv
from typing import Dict, Optional

load_dotenv(".env")
API_KEY = os.getenv("API_KEY")
BASE_URL = "https://api.apilayer.com/exchangerates_data/"


def convert_transaction_to_rub(transaction: Dict[str, str]) -> Optional[float]:
    """
    Конвертирует сумму транзакции в рубли.

    :param transaction: Словарь с данными транзакции, должен содержать ключи 'amount' и 'currency'
    :return: Сумма в рублях (float) или None в случае ошибки
    """
    if not API_KEY:
        print("Ошибка: API_KEY не найден в переменных окружения.")
        return None

    amount = float(transaction.get("amount", 0))
    currency = transaction.get("currency", "RUB").upper()

    # Если валюта уже рубли, возвращаем как есть
    if currency == "RUB":
        return amount

    # Поддерживаем только USD и EUR
    if currency not in ("USD", "EUR"):
        print(f"Ошибка: Валюта {currency} не поддерживается для конвертации")
        return None

    try:
        # Получаем текущий курс
        url = f"{BASE_URL}convert?to=RUB&from={currency}&amount={amount}"
        headers = {"apikey": API_KEY}

        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()

        if data.get("success"):
            return float(data["result"])
        else:
            print(f"API Error: {data.get('error', {}).get('info', 'Unknown error')}")
            return None

    except requests.exceptions.RequestException as e:
        print(f"Ошибка запроса к API: {e}")
        return None
    except ValueError as e:
        print(f"Ошибка декодирования JSON от API: {e}")
        return None
    except Exception as e:
        print(f"Неожиданная ошибка: {e}")
        return None

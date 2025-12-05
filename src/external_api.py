import os
import requests
from dotenv import load_dotenv
from typing import Dict, Any, Union

load_dotenv()
API_KEY: Union[str, None] = os.getenv("API_KEY")
BASE_URL: str = "https://api.apilayer.com/exchangerates_data/"


def convert_transaction_to_rub(transaction: Dict[str, Any]) -> float:
    """
    Конвертирует сумму транзакции в рубли.

    :param transaction: Словарь с данными транзакции
    :return: Сумма в рублях (float)
    :raises: ValueError в случае ошибок
    """
    if not API_KEY:
        raise ValueError("API_KEY не найден в переменных окружения")

    try:
        # Извлекаем amount и currency из структуры транзакции
        operation_amount: Dict[str, Any] = transaction.get("operationAmount", {})
        amount: float = float(operation_amount.get("amount", 0))
        currency_info: Dict[str, str] = operation_amount.get("currency", {})
        currency: str = currency_info.get("code", "RUB").upper()
    except (AttributeError, ValueError) as e:
        raise ValueError(f"Ошибка при парсинге транзакции: {e}")

    # Если валюта уже рубли, возвращаем как есть
    if currency == "RUB":
        return amount

    # Поддерживаем только USD и EUR
    if currency not in ("USD", "EUR"):
        raise ValueError(f"Валюта {currency} не поддерживается для конвертации")

    try:
        # Получаем текущий курс
        url: str = f"{BASE_URL}convert?to=RUB&from={currency}&amount={amount}"
        headers: Dict[str, str] = {"apikey": API_KEY}

        response: requests.Response = requests.get(url, headers=headers)
        response.raise_for_status()
        data: Dict[str, Any] = response.json()

        if data.get("success"):
            return float(data["result"])
        raise ValueError(f"API Error: {data.get('error', {}).get('info', 'Unknown error')}")

    except requests.exceptions.RequestException as e:
        raise ValueError(f"Ошибка запроса к API: {e}")
    except ValueError as e:
        raise ValueError(f"Ошибка декодирования JSON от API: {e}")
    except Exception as e:
        raise ValueError(f"Неожиданная ошибка: {e}")  # Добавляем обработку общего исключения

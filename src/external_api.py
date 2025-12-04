import os
import requests
from dotenv import load_dotenv
from typing import Optional, Dict, cast

load_dotenv(".env")
API_KEY = os.getenv("API_KEY")
# print(f"DEBUG: API Key loaded successfully? {'Yes' if API_KEY else 'No'}")
BASE_URL = "https://api.apilayer.com/exchangerates_data/"


def get_currency_rates(base_currency: str = "EUR", symbols: str = "RUB,USD") -> Optional[Dict[str, float]]:
    """
    Получает текущие курсы обмена валют (RUB и EUR) относительно базовой валюты (USD).
    """
    if not API_KEY:
        print("Ошибка: API_KEY не найден в переменных окружения.")
        return None

    url = f"{BASE_URL}latest?base={base_currency}&symbols={symbols}"

    headers = {"apikey": API_KEY}

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()

        if data.get("success"):
            rates_data = data.get('rates')
            return cast(Dict[str, float], rates_data)
        else:
            print(f"API Error: {data.get('error', {}).get('info', 'Unknown error')}")
            return None

    except requests.exceptions.RequestException as e:
        print(f"Ошибка запроса к API: {e}")
        return None
    except ValueError as e:
        print(f"Ошибка декодирования JSON от API: {e}")
        return None

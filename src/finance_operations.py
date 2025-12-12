import csv
import pandas as pd
from typing import List, Dict, Union, Any
from datetime import datetime


def convert_value(key: str, value: Any) -> Any:
    """
    Преобразует значение поля транзакции в нужный тип
    с обработкой NaN и None значений
    """
    if pd.isna(value) or value is None:
        return None

    try:
        if key == "id":
            return int(float(value)) if not pd.isna(value) else None
        elif key == "amount":
            return float(value) if not pd.isna(value) else None
        elif key == "date":
            if pd.isna(value):
                return None
            if isinstance(value, str):
                return datetime.fromisoformat(value.replace("Z", "+00:00"))
            return value.to_pydatetime() if hasattr(value, "to_pydatetime") else value
        return str(value) if not pd.isna(value) else None
    except (ValueError, TypeError):
        return None


def convert_transaction(transaction: Dict) -> Dict:
    """Приводит все значения транзакции к правильным типам с обработкой NaN"""
    return {k: convert_value(k, v) for k, v in transaction.items()}


def read_csv_transactions(file_path: str) -> List[Dict]:
    """
    Читает финансовые операции из CSV файла

    :param file_path: Путь к CSV файлу
    :return: Список словарей с транзакциями (с правильными типами данных)
    """
    transactions = []

    with open(file_path, mode="r", encoding="utf-8") as file:
        reader = csv.DictReader(file, delimiter=";")
        for row in reader:
            transactions.append(convert_transaction(row))

    return [t for t in transactions if any(v is not None for v in t.values())]


def read_excel_transactions(file_path: str, sheet_name: Union[int, str, None] = 0) -> List[Dict]:
    """
    Читает финансовые операции из Excel файла

    :param file_path: Путь к Excel файлу
    :param sheet_name: Номер листа (int), название (str) или None (по умолчанию: 0 - первый лист)
    :return: Список словарей с транзакциями (с правильными типами данных)
    """
    try:
        df = pd.read_excel(file_path, sheet_name=sheet_name, engine="openpyxl")

        # Если вернулся словарь (при sheet_name=None), возьмем первый лист
        if isinstance(df, dict):
            df = list(df.values())[0]

        if not isinstance(df, pd.DataFrame):
            raise ValueError("Прочитанные данные не являются таблицей")

        # Конвертируем DataFrame, фильтруя пустые строки
        transactions = [convert_transaction(record) for record in df.to_dict("records")]
        return [t for t in transactions if any(v is not None for v in t.values())]

    except Exception as e:
        print(f"Ошибка чтения Excel файла: {e}")
        return []

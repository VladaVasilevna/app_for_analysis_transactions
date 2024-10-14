import json
import os
from datetime import datetime, timedelta
from typing import Any, Dict, List

import pandas as pd
import requests

API_TOKEN = os.getenv("API_TOKEN")


def read_excel_data(file_path: str) -> pd.DataFrame:
    """Чтение данных из Excel файла."""
    return pd.read_excel(file_path)


def get_user_settings(settings_path: str) -> Dict[str, List[str]]:
    """Получение пользовательских настроек из JSON файла."""
    try:
        with open(settings_path, "r", encoding="utf-8") as f:
            settings = json.load(f)

        if not isinstance(settings, dict):
            raise ValueError("Настройки должны быть словарём.")

        for key, value in settings.items():
            if not isinstance(value, list) or not all(isinstance(item, str) for item in value):
                raise ValueError(f"Значение для ключа '{key}' должно быть списком строк.")

        return settings
    except (FileNotFoundError, json.JSONDecodeError) as e:
        raise ValueError(f"Ошибка при чтении настроек: {e}")


def fetch_currency_rates(currencies: List[str]) -> List[Dict[str, float]]:
    """Получение курсов валют с API."""
    url = "https://api.exchangeratesapi.io/latest?base=EUR"

    try:
        response = requests.get(url)
        response.raise_for_status()  # Проверка на ошибки HTTP
        data = response.json()

        # Проверка наличия ключа 'rates'
        if "rates" not in data:
            print("Ключ 'rates' отсутствует в ответе API.")
            return []

        rates = []
        for currency in currencies:
            if currency in data["rates"]:
                rates.append({"currency": currency, "rate": data["rates"][currency]})

        return rates
    except requests.RequestException as e:
        print(f"Ошибка при получении курсов валют: {e}")
        return []


def fetch_stock_prices(stocks: List[str]) -> List[Dict[str, float]]:
    """Получение цен акций из API."""
    stock_prices = []

    for stock in stocks:
        response = requests.get(f"https://api.example.com/stocks/{stock}?token={API_TOKEN}")
        stock_data = response.json()
        stock_prices.append({"stock": stock, "price": stock_data["price"]})

    return stock_prices


def process_transactions(
    data: pd.DataFrame, input_date: str, period: str, user_settings: Dict[str, List[str]]
) -> Dict[str, Any]:
    """Обработка транзакций и генерация JSON ответа."""

    # Проверка наличия необходимых столбцов
    required_columns = ["Дата операции", "Тип", "Сумма", "Категория"]
    for column in required_columns:
        if column not in data.columns:
            raise ValueError(f"Отсутствует необходимый столбец: {column}")

    target_date = datetime.strptime(input_date, "%Y-%m-%d %H:%M:%S")

    if period == "W":
        start_date = target_date - timedelta(days=target_date.weekday())
        end_date = target_date
    elif period == "M":
        start_date = target_date.replace(day=1)
        end_date = target_date
    elif period == "Y":
        start_date = target_date.replace(month=1, day=1)
        end_date = target_date
    else:  # ALL
        start_date = datetime.min
        end_date = target_date

    filtered_data = data[(data["Дата операции"] >= start_date) & (data["Дата операции"] <= end_date)]

    # Проверка на наличие строк после фильтрации
    if filtered_data.empty:
        return {
            "expenses": {"total_amount": 0, "main": [], "transfers_and_cash": []},
            "income": {"total_amount": 0, "main": []},
            "currency_rates": [],
            "stock_prices": [],
        }

    expenses_total = round(filtered_data[filtered_data["Тип"] == "Расход"]["Сумма"].sum())

    expenses_by_category = (
        filtered_data[filtered_data["Тип"] == "Расход"]
        .groupby("Категория")["Сумма"]
        .sum()
        .reset_index()
        .sort_values(by="Сумма", ascending=False)
    )

    main_expenses = expenses_by_category.head(7)

    other_expenses_sum = expenses_by_category.iloc[7:]["Сумма"].sum()

    if other_expenses_sum > 0:
        other_expenses_df = pd.DataFrame([{"Категория": "Остальное", "Сумма": other_expenses_sum}])
        main_expenses = pd.concat([main_expenses, other_expenses_df], ignore_index=True)

    transfers_and_cash = (
        filtered_data[filtered_data["Тип"] == "Расход"]
        .groupby("Категория")["Сумма"]
        .sum()
        .reindex(["Наличные", "Переводы"])  # Используйте reindex для избежания ошибок
        .fillna(0)  # Заполните отсутствующие значения нулями
        .reset_index()
    )

    income_total = round(filtered_data[filtered_data["Тип"] == "Поступление"]["Сумма"].sum())

    income_by_category = (
        filtered_data[filtered_data["Тип"] == "Поступление"]
        .groupby("Категория")["Сумма"]
        .sum()
        .reset_index()
        .sort_values(by="Сумма", ascending=False)
    )

    response_json: Dict[str, Any] = {
        "expenses": {
            "total_amount": expenses_total,
            "main": main_expenses.to_dict(orient="records"),
            "transfers_and_cash": transfers_and_cash.to_dict(orient="records"),
        },
        "income": {"total_amount": income_total, "main": income_by_category.to_dict(orient="records")},
        "currency_rates": fetch_currency_rates(user_settings.get("user_currencies", [])),
        # Предполагается, что fetch_stock_prices также определена в вашем коде.
        "stock_prices": fetch_stock_prices(user_settings.get("user_stocks", [])),
    }

    return response_json

import json
import logging
import os
from datetime import datetime
from typing import Any, Dict, List

import pandas as pd
import requests
from dotenv import load_dotenv

from views import generate_greeting, prepare_response

# Настройка логирования
logging.basicConfig(level=logging.INFO)

# Загрузка переменных окружения из файла .env
load_dotenv()
API_TOKEN = os.getenv("API_TOKEN")  # Получаем API токен

# Проверка наличия токена
if API_TOKEN is None:
    raise ValueError("API_TOKEN не установлен. Проверьте файл .env.")


def read_excel_data(file_path: str) -> pd.DataFrame:
    """Чтение данных из Excel файла."""
    logging.info(f"Чтение данных из файла: {file_path}")
    return pd.read_excel(file_path)


def get_user_settings(file_path: str) -> Dict[str, Any]:
    """Получение пользовательских настроек из JSON файла."""
    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)


def process_transactions(
    transactions_data: pd.DataFrame, input_datetime: str, user_settings: Dict[str, Any]
) -> Dict[str, Any]:
    """Обработка транзакций и формирование результата."""

    # Преобразование строки даты во время
    input_time = datetime.strptime(input_datetime, "%Y-%m-%d %H:%M:%S")

    # Определение начала и конца периода на основе входной даты (по умолчанию месяц)
    start_date = input_time.replace(day=1)
    end_date = start_date.replace(month=start_date.month % 12 + 1) - pd.Timedelta(days=1)

    # Фильтрация транзакций по дате
    filtered_transactions = transactions_data[
        (transactions_data["Дата операции"] >= start_date.strftime("%d.%m.%Y"))
        & (transactions_data["Дата операции"] <= end_date.strftime("%d.%m.%Y"))
    ]

    # Генерация информации по картам
    cards_info = analyze_cards(filtered_transactions)

    # Получение топ-5 транзакций
    top_transactions = get_top_transactions(filtered_transactions)

    # Получение курсов валют и цен акций
    currency_rates = fetch_currency_rates(user_settings.get("user_currencies", []))
    stock_prices = fetch_stock_prices(user_settings.get("user_stocks", []))

    # Формирование JSON ответа
    response = prepare_response(
        generate_greeting(input_time), cards_info, top_transactions, currency_rates, stock_prices
    )

    return response


def analyze_cards(operations: pd.DataFrame) -> List[Dict[str, float]]:
    """Анализ операций по картам."""
    logging.info("Анализ операций по картам")

    card_summary = (
        operations.groupby("Номер карты")
        .agg(
            last_digits=("Номер карты", "first"),
            total_spent=("Сумма операции с округлением", "sum"),
            cashback=("Сумма операции с округлением", lambda x: round(x.sum() * 0.01, 2)),
        )
        .reset_index()
    )

    return card_summary[["last_digits", "total_spent", "cashback"]].to_dict(orient="records")


def get_top_transactions(operations: pd.DataFrame) -> List[Dict[str, Any]]:
    """Получение топ-5 транзакций по сумме платежа."""
    logging.info("Получение топ-5 транзакций")

    top_transactions = operations.nlargest(5, "Сумма платежа")[
        ["Дата операции", "Сумма платежа", "Категория", "Описание"]
    ]

    return top_transactions.to_dict(orient="records")


def fetch_currency_rates(currencies: List[str]) -> List[Dict[str, float]]:
    """Получение курсов валют с API."""

    url = f"https://api.apilayer.com/exchangerates_data/latest?base=RUB&symbols={','.join(currencies)}"

    headers = {"apikey": API_TOKEN}

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()

        data = response.json()

        if "rates" not in data:
            logging.error("Ключ 'rates' отсутствует в ответе API.")
            return []

        rates = []
        for currency in currencies:
            if currency in data["rates"]:
                rates.append({"currency": currency, "rate": round(data["rates"][currency], 4)})

        return rates

    except requests.RequestException as e:
        logging.error(f"Ошибка при получении курсов валют: {e}")
        return []


def fetch_stock_prices(stocks: List[str]) -> List[Dict[str, float]]:
    """Получение цен акций из API."""

    stock_prices = []

    for stock in stocks:
        try:
            response = requests.get(f"https://api.apilayer.com/stock_data/{stock}?apikey={API_TOKEN}")

            response.raise_for_status()

            stock_data = response.json()
            if "price" in stock_data:
                stock_prices.append({"stock": stock, "price": stock_data["price"]})
            else:
                logging.warning(f"Нет цены для {stock} в ответе API.")

        except requests.RequestException as e:
            logging.error(f"Ошибка при получении данных для {stock}: {e}")

    return stock_prices

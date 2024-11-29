import logging
import os
from typing import Any, Dict, List, Optional

import pandas as pd
import requests
from dotenv import load_dotenv

# Настройка логирования
logging.basicConfig(level=logging.INFO)

# Загрузка переменных окружения из файла .env
load_dotenv()
API_TOKEN: Optional[str] = os.getenv("API_TOKEN")  # Получаем API токен для валют
API_KEY: Optional[str] = os.getenv("API_KEY")  # Получаем API ключ для акций

# Проверка наличия токена
if API_TOKEN is None:
    raise ValueError("API_TOKEN не установлен. Проверьте файл .env.")

if API_KEY is None:
    raise ValueError("API_KEY не установлен. Проверьте файл .env.")


def read_excel_data(file_path: str) -> Optional[pd.DataFrame]:
    """Читает данные из XLSX файла и возвращает DataFrame или None."""
    try:
        df = pd.read_excel(file_path)
        return df
    except Exception as e:
        logging.error(f"Ошибка при чтении файла: {e}")
        return None


def get_currency_rates(user_currencies: List[str]) -> List[Dict[str, Any]]:
    """Получает курсы валют через APIlayer."""
    rates = []
    api_url = "https://api.apilayer.com/exchangerates_data/latest"
    headers = {"apikey": API_TOKEN}

    response = requests.get(api_url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        for currency in user_currencies:
            if currency in data["rates"]:
                rates.append({"currency": currency, "rate": data["rates"][currency]})
    else:
        logging.error("Ошибка при получении курсов валют.")

    return rates


def get_stock_prices(stocks: List[str]) -> List[Dict[str, Any]]:
    """Получает цены акций с использованием Marketstack."""
    stock_prices = []

    url = "https://api.marketstack.com/v1/intraday"

    for stock in stocks:
        querystring = {"access_key": API_KEY, "symbols": stock}

        try:
            response = requests.get(url, params=querystring)
            response.raise_for_status()

            stock_data = response.json()
            if "data" in stock_data and len(stock_data["data"]) > 0:
                last_price = stock_data["data"][0]["last"]
                if last_price is not None:
                    stock_prices.append({"stock": stock, "price": float(last_price)})
                else:
                    logging.error(f"Цена для акции {stock} равна None.")
            else:
                logging.error(f"Нет данных для акции {stock}.")

        except requests.RequestException as e:
            logging.error(f"Ошибка при получении данных для {stock}: {e}")

    return stock_prices

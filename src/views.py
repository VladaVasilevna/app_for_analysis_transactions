from datetime import datetime
from typing import Any, Dict

import pandas as pd

from src.utils import get_currency_rates, get_stock_prices, read_excel_data


def generate_response(date_str: str, user_settings: Dict[str, Any]) -> Dict[str, Any]:
    """Генерирует JSON-ответ на основе входной даты."""

    while True:
        current_time: datetime = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")

        # Приветствие
        if current_time.hour < 6:
            greeting: str = "Доброй ночи"
        elif current_time.hour < 12:
            greeting = "Доброе утро"
        elif current_time.hour < 18:
            greeting = "Добрый день"
        else:
            greeting = "Добрый вечер"

        # Чтение данных из XLSX файла
        df = read_excel_data("../data/operations.xlsx")

        # Обработка данных
        if df is not None:
            # Определение начала месяца
            month_start = current_time.replace(day=1)

            # Фильтрация данных по началу месяца и введенной дате
            filtered_df = df[
                (pd.to_datetime(df["Дата операции"], dayfirst=True) >= month_start)
                & (pd.to_datetime(df["Дата операции"], dayfirst=True) <= current_time)
            ].copy()

            # Проверка наличия транзакций
            if filtered_df.empty:
                print("Дата не найдена. Введите другую дату.")
                date_str = input("Введите дату в формате YYYY-MM-DD HH:MM:SS: ")
                continue

            # Обработка карт и кешбэка
            cards_summary = (
                filtered_df.groupby("Номер карты")
                .agg(
                    last_digits=("Номер карты", "first"),
                    total_spent=("Сумма операции", lambda x: round(-x[x < 0].sum(), 2)),
                    cashback=("Сумма операции", lambda x: round(-x[x < 0].sum() * 0.01, 2)),
                )
                .reset_index()
            )

            cards_summary = cards_summary[["last_digits", "total_spent", "cashback"]]

            # Добавляем временную колонку с абсолютными значениями
            filtered_df.loc[:, "absolute_amount"] = filtered_df["Сумма платежа"].abs()

            # Выбираем топ-5 транзакций по абсолютному значению
            top_transactions = filtered_df.nlargest(5, "absolute_amount").assign(
                date=lambda temp_df: pd.to_datetime(temp_df["Дата операции"], dayfirst=True).dt.strftime("%d.%m.%Y"),
                amount=lambda temp_df: temp_df["Сумма платежа"],
                category=lambda temp_df: temp_df["Категория"],
                description=lambda temp_df: temp_df["Описание"],
            )[["date", "amount", "category", "description"]]

            # Удаляем временную колонку
            filtered_df.drop(columns=["absolute_amount"], inplace=True)

            # Получение курсов валют и цен акций
            currency_rates = get_currency_rates(user_settings["user_currencies"])
            stock_prices = get_stock_prices(user_settings["user_stocks"])

            # Формирование JSON-ответа
            response_json: Dict[str, Any] = {
                "greeting": greeting,
                "cards": cards_summary.to_dict(orient="records"),
                "top_transactions": top_transactions.to_dict(orient="records"),
                "currency_rates": currency_rates,
                "stock_prices": stock_prices,
            }

            return response_json

        return {"error": "Данные о транзакциях недоступны."}

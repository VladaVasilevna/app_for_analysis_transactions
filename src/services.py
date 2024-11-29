import logging
from datetime import datetime
from typing import Any, Dict, List

import pandas as pd

# Настройка логирования
logging.basicConfig(level=logging.INFO)


def investment_bank(month: str, transactions: List[Dict[str, Any]], limit: int) -> float:
    """Вычисляет сумму, отложенную в 'Инвесткопилку' за указанный месяц."""
    total_saved = 0.0

    # Преобразуем строку месяца в объект datetime для проверки
    month_start = datetime.strptime(month, "%Y-%m")
    next_month = (month_start.replace(day=1) + pd.DateOffset(months=1)).replace(day=1)

    logging.info(f"Округляем транзакции до {limit} в Инвесткопилку")

    for transaction in transactions:
        transaction_date_str = transaction.get("Дата операции")
        transaction_amount = transaction.get("Сумма операции")

        if transaction_date_str and transaction_amount is not None:
            # Попробуем разобрать дату в обоих форматах
            try:
                transaction_date = datetime.strptime(transaction_date_str, "%Y-%m-%d %H:%M:%S")
            except ValueError:
                transaction_date = datetime.strptime(transaction_date_str, "%d.%m.%Y %H:%M:%S")

            # Проверяем, попадает ли транзакция в указанный месяц
            if month_start <= transaction_date < next_month:
                rounded_amount = ((transaction_amount // limit) + 1) * limit
                saved_amount = rounded_amount - transaction_amount
                total_saved += saved_amount

    return total_saved

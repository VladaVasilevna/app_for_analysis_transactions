import logging
from datetime import datetime
from typing import Any, Dict, List, Optional

import pandas as pd

# Настройка логирования
logging.basicConfig(level=logging.INFO)


def investment_bank(month: str, transactions: List[Dict[str, Any]], limit: int) -> Optional[float]:
    """Вычисляет сумму, отложенную в 'Инвесткопилку' за указанный месяц."""
    total_saved = 0.0

    # Преобразуем строку месяца в объект datetime для проверки
    month_start = datetime.strptime(month, "%Y-%m")
    next_month = (month_start.replace(day=1) + pd.DateOffset(months=1)).replace(day=1)

    # Фильтрация транзакций по указанному месяцу
    monthly_transactions = [
        transaction
        for transaction in transactions
        if transaction.get("Дата операции")
        and month_start <= datetime.strptime(transaction["Дата операции"], "%d.%m.%Y %H:%M:%S") < next_month
    ]

    # Проверка наличия транзакций за указанный месяц
    if not monthly_transactions:
        logging.warning("Нет транзакций за указанный месяц.")
        return None

    logging.info(f"Округляем транзакции до {limit} в Инвесткопилку")

    for transaction in monthly_transactions:
        transaction_date_str = transaction.get("Дата операции")
        transaction_amount = transaction.get("Сумма операции")

        if transaction_date_str and transaction_amount is not None:
            try:
                # Пробуем разобрать дату в обоих форматах
                transaction_date = datetime.strptime(transaction_date_str, "%d.%m.%Y %H:%M:%S")
            except ValueError:
                logging.error(f"Некорректный формат даты: {transaction_date_str}")
                continue

            if month_start <= transaction_date < next_month and transaction_amount < 0:
                abs_transaction_amount = abs(transaction_amount)
                remainder = abs_transaction_amount % limit

                if remainder == 0:
                    continue  # Если остаток 0, не округляем

                # Определяем округленное значение
                rounded_amount = (abs_transaction_amount // limit + 1) * limit

                # Вычисляем сумму, которую нужно отложить
                saved_amount = rounded_amount + transaction_amount
                total_saved += saved_amount

    return total_saved

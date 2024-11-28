import json
import logging
from datetime import datetime, timedelta
from typing import Any, Callable, Dict, Optional

import pandas as pd

# Настройка логирования
logging.basicConfig(level=logging.INFO)


def report_decorator(func: Callable[..., Any]) -> Callable[..., Any]:
    """Декоратор для записи отчета в файл с названием по умолчанию."""

    def wrapper(*args: Any, **kwargs: Any) -> Any:
        result = func(*args, **kwargs)
        # Генерация имени файла на основе текущей даты и времени
        filename = f"spending_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        # Запись результата в файл
        try:
            with open(filename, "w", encoding="utf-8") as f:
                json.dump(result, f, ensure_ascii=False, indent=4)
            logging.info(f"Отчет сохранен в файл: {filename}")
        except Exception as e:
            logging.error(f"Ошибка при сохранении отчета: {e}")
        return result

    return wrapper


def report_decorator_with_filename(filename: str) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    """Декоратор для записи отчета в файл с заданным именем."""

    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            result = func(*args, **kwargs)
            # Запись результата в указанный файл
            try:
                with open(filename, "w", encoding="utf-8") as f:
                    json.dump(result, f, ensure_ascii=False, indent=4)
                logging.info(f"Отчет сохранен в файл: {filename}")
            except Exception as e:
                logging.error(f"Ошибка при сохранении отчета: {e}")
            return result

        return wrapper

    return decorator


@report_decorator
def spending_by_category(transactions: pd.DataFrame, category: str, date: Optional[str] = None) -> Dict[str, Any]:
    """Возвращает траты по заданной категории за последние три месяца."""

    # Установка текущей даты, если дата не передана
    if date is None:
        date = datetime.now().strftime("%Y-%m-%d")

    # Преобразование строки даты в объект datetime
    current_date = datetime.strptime(date, "%Y-%m-%d")

    # Определение даты начала периода (3 месяца назад)
    start_date = current_date - timedelta(days=90)

    # Фильтрация транзакций по категории и дате
    filtered_transactions = transactions[
        (transactions["Категория"] == category)
        & (transactions["Дата операции"] >= start_date)
        & (transactions["Дата операции"] <= current_date)
    ]

    # Подсчет сумм по тратам
    total_spent = filtered_transactions["Сумма операции с округлением"].sum()

    # Формирование результата в формате словаря
    report_data = {
        "category": category,
        "total_spent": total_spent,
        "date_range": {"start_date": start_date.strftime("%Y-%m-%d"), "end_date": current_date.strftime("%Y-%m-%d")},
    }

    return report_data

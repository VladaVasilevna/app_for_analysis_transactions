from datetime import datetime
from typing import Any, Dict, List


def generate_greeting(current_time: datetime) -> str:
    """Генерация приветствия в зависимости от времени суток."""
    hour = current_time.hour
    if hour < 6:
        return "Доброй ночи"
    elif hour < 12:
        return "Доброе утро"
    elif hour < 18:
        return "Добрый день"
    else:
        return "Добрый вечер"


def prepare_response(greeting: str, cards_info: List[Dict[str, float]], top_transactions: List[Dict[str, float]],
                     currency_rates: List[Dict[str, float]], stock_prices: List[Dict[str, float]]) -> Dict[str, Any]:
    """Формирование JSON ответа."""
    return {
        "greeting": greeting,
        "cards": cards_info,
        "top_transactions": top_transactions,
        "currency_rates": currency_rates,
        "stock_prices": stock_prices,
    }

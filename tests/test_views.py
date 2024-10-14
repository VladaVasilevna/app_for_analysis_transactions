from datetime import datetime
from typing import Any, Dict, List

from src.views import generate_greeting, prepare_response


def test_generate_greeting() -> None:
    """Тестирование генерации приветствия в зависимости от времени суток."""
    assert generate_greeting(datetime(2024, 10, 14, 5)) == "Доброй ночи"
    assert generate_greeting(datetime(2024, 10, 14, 10)) == "Доброе утро"
    assert generate_greeting(datetime(2024, 10, 14, 15)) == "Добрый день"
    assert generate_greeting(datetime(2024, 10, 14, 19)) == "Добрый вечер"


def test_prepare_response() -> None:
    """Тестирование формирования JSON ответа."""
    greeting: str = "Доброе утро"

    # Изменены аннотации типов
    cards_info: List[Dict[str, Any]] = [{"name": "Card1", "value": 100}]
    top_transactions: List[Dict[str, Any]] = [{"transaction": "Trans1", "amount": 200}]

    response: Dict[str, Any] = prepare_response(greeting, cards_info, top_transactions, [], [])

    assert response["greeting"] == greeting
    assert len(response["cards"]) == len(cards_info)
    assert len(response["top_transactions"]) == len(top_transactions)

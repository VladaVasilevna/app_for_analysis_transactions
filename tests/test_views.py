from datetime import datetime
from typing import Any, Dict, List

import pytest

from src.views import generate_greeting, prepare_response


# Фикстура для подготовки данных для теста prepare_response
@pytest.fixture
def response_data() -> Dict[str, Any]:
    """Фикстура для подготовки данных ответа."""
    greeting: str = "Доброе утро"
    cards_info: List[Dict[str, Any]] = [{"name": "Card1", "value": 100}]
    top_transactions: List[Dict[str, Any]] = [{"transaction": "Trans1", "amount": 200}]

    return {
        "greeting": greeting,
        "cards_info": cards_info,
        "top_transactions": top_transactions,
        "currency_rates": [],
        "stock_prices": [],
    }


@pytest.mark.parametrize(
    "time, expected_greeting",
    [
        (datetime(2024, 10, 14, 5), "Доброй ночи"),
        (datetime(2024, 10, 14, 10), "Доброе утро"),
        (datetime(2024, 10, 14, 15), "Добрый день"),
        (datetime(2024, 10, 14, 19), "Добрый вечер"),
    ],
)
def test_generate_greeting(time: datetime, expected_greeting: str) -> None:
    """Тестирование генерации приветствия в зависимости от времени суток."""
    assert generate_greeting(time) == expected_greeting


def test_prepare_response(response_data: Dict[str, Any]) -> None:
    """Тестирование формирования JSON ответа."""

    response: Dict[str, Any] = prepare_response(
        response_data["greeting"],
        response_data["cards_info"],
        response_data["top_transactions"],
        response_data["currency_rates"],
        response_data["stock_prices"],
    )

    assert response["greeting"] == response_data["greeting"]
    assert len(response["cards"]) == len(response_data["cards_info"])
    assert len(response["top_transactions"]) == len(response_data["top_transactions"])

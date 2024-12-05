from typing import Any, Dict
from unittest.mock import patch

import pandas as pd

from src.views import generate_response

# Пример данных для теста
mock_excel_data = pd.DataFrame(
    {
        "Дата операции": pd.to_datetime(["2024-01-01", "2024-01-15", "2024-01-20"]),
        "Номер карты": ["1234", "5678", "1234"],
        "Сумма операции": [-100.0, -150.0, -200.0],
        "Сумма платежа": [-100.0, -150.0, -200.0],
        "Категория": ["Еда", "Транспорт", "Развлечения"],
        "Описание": ["Обед", "Такси", "Кино"],
    }
)

user_settings = {"user_currencies": ["USD", "EUR"], "user_stocks": ["AAPL", "GOOGL"]}


def test_generate_response() -> None:
    with patch("src.views.read_excel_data", return_value=mock_excel_data):
        response: Dict[str, Any] = generate_response("2024-01-20 12:00:00", user_settings)

        # Проверка приветствия
        assert response["greeting"] == "Добрый день"

        # Проверка наличия карт
        cards = response["cards"]
        assert len(cards) == 2

        # Проверка значений для каждой карты
        card_1234 = next((card for card in cards if card["last_digits"] == "1234"), None)
        card_5678 = next((card for card in cards if card["last_digits"] == "5678"), None)

        assert card_1234 is not None
        assert card_1234["total_spent"] == 300.0  # общая сумма расходов по карте (100 + 200)
        assert card_1234["cashback"] == 3.0

        assert card_5678 is not None
        assert card_5678["total_spent"] == 150.0
        assert card_5678["cashback"] == 1.5

        # Проверка топ-транзакций
        top_transactions = response["top_transactions"]
        assert len(top_transactions) == 3  # Должны быть три транзакции в диапазоне

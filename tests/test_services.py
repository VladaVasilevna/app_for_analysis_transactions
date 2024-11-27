from typing import Any, Dict, List

from src.services import investment_bank


def test_investment_bank() -> None:
    """Тестирует функцию investment_bank с обычным форматом даты."""
    transactions: List[Dict[str, Any]] = [
        {"Дата операции": "2024-01-05 12:00:00", "Сумма операции": 1712},
        {"Дата операции": "2024-01-15 15:30:00", "Сумма операции": 845},
        {"Дата операции": "2024-01-20 10:00:00", "Сумма операции": 1234},
        {"Дата операции": "2024-02-01 09:00:00", "Сумма операции": 500},
    ]

    result: float = investment_bank("2024-01", transactions, 50)

    expected_saved: float = 38 + 5 + 16
    assert result == expected_saved


def test_investment_bank_with_different_format() -> None:
    """Тестирует функцию investment_bank с форматом даты DD.MM.YYYY."""
    transactions: List[Dict[str, Any]] = [
        {"Дата операции": "31.12.2021 16:44:00", "Сумма операции": 1712},
        {"Дата операции": "15.01.2022 15:30:00", "Сумма операции": 845},
        {"Дата операции": "20.01.2022 10:00:00", "Сумма операции": 1234},
        {"Дата операции": "01.02.2022 09:00:00", "Сумма операции": 500},
    ]

    result: float = investment_bank("2022-01", transactions, 50)

    expected_saved: float = 5 + 16
    assert result == expected_saved

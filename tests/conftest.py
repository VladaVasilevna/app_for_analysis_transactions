from typing import Any, Dict
from unittest import mock

import pandas as pd
import pytest


@pytest.fixture
def user_settings() -> Dict[str, Any]:
    """Фикстура для загрузки пользовательских настроек из JSON файла."""
    return {"user_currencies": ["USD", "EUR"], "user_stocks": ["AAPL", "GOOGL"]}


@pytest.fixture
def mock_excel_data() -> pd.DataFrame:
    """Фикстура для создания тестовых данных Excel."""
    data: Dict[str, Any] = {
        "Дата операции": pd.to_datetime(["2024-01-01", "2024-01-15", "2024-01-20"]),
        "Номер карты": ["1234", "5678", "1234"],
        "Сумма операции": [100.0, 150.0, 200.0],
        "Сумма платежа": [-100.0, -150.0, -200.0],
        "Категория": ["Еда", "Транспорт", "Развлечения"],
        "Описание": ["Обед", "Такси", "Кино"],
    }
    return pd.DataFrame(data)


@pytest.fixture
def mock_function() -> mock.Mock:
    """Фикстура для создания мок-функции."""
    return mock.Mock(return_value={"data": "test report"})


@pytest.fixture
def transactions() -> pd.DataFrame:
    """Фикстура для создания тестовых данных транзакций."""
    data: Dict[str, Any] = {
        "Дата операции": ["01.09.2024 12:00:00", "15.09.2024 14:30:00", "10.10.2024 09:00:00", "20.11.2024 11:00:00"],
        "Категория": ["Продукты", "Продукты", "Развлечения", "Продукты"],
        "Сумма операции": ["1000,50", "2000,00", "1500,75", "500,25"],
    }
    return pd.DataFrame(data)

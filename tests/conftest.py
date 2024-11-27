from typing import Any, Dict

import pandas as pd
import pytest


@pytest.fixture
def user_settings() -> Dict[str, Any]:
    """Фикстура для загрузки пользовательских настроек из JSON файла."""
    return {"user_currencies": ["USD", "EUR"], "user_stocks": ["AAPL", "GOOGL"]}


@pytest.fixture
def mock_excel_data() -> pd.DataFrame:
    """Фикстура для создания тестовых данных Excel."""
    data = {
        "Дата операции": pd.to_datetime(["2024-01-01", "2024-01-15", "2024-01-20"]),
        "Номер карты": ["1234", "5678", "1234"],
        "Сумма операции с округлением": [100.0, 150.0, 200.0],
        "Сумма платежа": [-100.0, -150.0, -200.0],
        "Категория": ["Еда", "Транспорт", "Развлечения"],
        "Описание": ["Обед", "Такси", "Кино"],
    }
    return pd.DataFrame(data)

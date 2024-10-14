import json
import os
from typing import Any, Dict, List
from unittest.mock import Mock, patch

import pandas as pd
import pytest

from src.utils import (fetch_currency_rates, fetch_stock_prices, get_user_settings, process_transactions,
                       read_excel_data)


def test_read_excel_data() -> None:
    """Тестирование чтения данных из Excel файла."""
    # Создаем тестовый DataFrame
    test_df = pd.DataFrame({"Column1": [1, 2], "Column2": [3, 4]})
    test_file_path = "test_data.xlsx"  # Путь к тестовому файлу

    # Сохраняем DataFrame в Excel файл
    test_df.to_excel(test_file_path, index=False)

    # Читаем данные из файла
    result = read_excel_data(test_file_path)

    # Проверяем, что считанные данные совпадают с оригинальными
    pd.testing.assert_frame_equal(result, test_df)

    # Удаляем тестовый файл после проверки
    os.remove(test_file_path)


def test_get_user_settings_valid() -> None:
    """Тестирование получения корректных пользовательских настроек."""
    settings_data: Dict[str, List[str]] = {"theme": ["dark"], "notifications": ["email", "sms"]}

    with open("test_settings.json", "w", encoding="utf-8") as f:
        json.dump(settings_data, f)

    result = get_user_settings("test_settings.json")
    assert result == settings_data


def test_get_user_settings_invalid_json() -> None:
    """Тестирование обработки некорректного JSON файла."""

    with open("invalid_settings.json", "w") as f:
        f.write("{invalid_json}")

    with pytest.raises(ValueError):
        get_user_settings("invalid_settings.json")


@patch("requests.get")
def test_fetch_currency_rates(mock_get: Mock) -> None:
    """Тестирование получения курсов валют."""
    mock_get.return_value.json.return_value = {"rates": {"USD": 1.1, "EUR": 0.9}}

    result = fetch_currency_rates(["USD", "EUR"])
    assert result == [{"currency": "USD", "rate": 1.1}, {"currency": "EUR", "rate": 0.9}]


@patch("requests.get")
def test_fetch_stock_prices(mock_get: Mock) -> None:
    """Тестирование получения цен акций."""
    mock_get.return_value.json.return_value = {"price": 100.0}

    result = fetch_stock_prices(["AAPL"])
    assert result == [{"stock": "AAPL", "price": 100.0}]


def test_process_transactions_() -> None:
    """Объединенный тест для обработки различных сценариев транзакций."""

    # Только расходы
    data1 = pd.DataFrame(
        {
            "Дата операции": pd.to_datetime(["2023-10-01", "2023-10-02"]),
            "Тип": ["Расход", "Расход"],
            "Сумма": [100, 50],
            "Категория": ["Еда", "Транспорт"],
        }
    )

    user_settings: Dict[str, Any] = {"user_currencies": ["USD"], "user_stocks": []}

    result1 = process_transactions(data1, "2023-10-02 00:00:00", "D", user_settings)

    assert result1["expenses"]["total_amount"] == 150
    assert len(result1["expenses"]["main"]) == 2

    # Только поступления
    data2 = pd.DataFrame(
        {
            "Дата операции": pd.to_datetime(["2023-10-01", "2023-10-02"]),
            "Тип": ["Поступление", "Поступление"],
            "Сумма": [200, 300],
            "Категория": ["Зарплата", "Подарок"],
        }
    )

    result2 = process_transactions(data2, "2023-10-02 00:00:00", "D", user_settings)

    assert result2["income"]["total_amount"] == 500
    assert len(result2["income"]["main"]) == 2

    # Смешанные транзакции
    data3 = pd.DataFrame(
        {
            "Дата операции": pd.to_datetime(["2023-10-01", "2023-10-02", "2023-10-02"]),
            "Тип": ["Расход", "Поступление", "Расход"],
            "Сумма": [100, 200, 50],
            "Категория": ["Еда", "Зарплата", "Наличные"],
        }
    )

    result3 = process_transactions(data3, "2023-10-02 00:00:00", "D", user_settings)

    assert result3["expenses"]["total_amount"] == 150
    assert result3["income"]["total_amount"] == 200
    assert len(result3["expenses"]["main"]) >= 1
    assert any(expense["Категория"] == "Наличные" for expense in result3["expenses"]["transfers_and_cash"])

    # Нет транзакций
    data4 = pd.DataFrame(columns=["Дата операции", "Тип", "Сумма", "Категория"])

    result4 = process_transactions(data4, "2023-10-02 00:00:00", "D", user_settings)

    assert result4["expenses"]["total_amount"] == 0
    assert result4["income"]["total_amount"] == 0

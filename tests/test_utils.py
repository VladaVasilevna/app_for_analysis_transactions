import json
import os
from typing import Any, Dict, Generator, List
from unittest.mock import Mock, patch

import pandas as pd
import pytest

from src.utils import (fetch_currency_rates, fetch_stock_prices, get_user_settings, process_transactions,
                       read_excel_data)


# Фикстура для создания тестового Excel файла
@pytest.fixture
def test_excel_file() -> Generator[str, None, None]:
    """Создает тестовый Excel файл и возвращает его путь."""
    test_df = pd.DataFrame({"Column1": [1, 2], "Column2": [3, 4]})
    test_file_path = "test_data.xlsx"
    test_df.to_excel(test_file_path, index=False)
    yield test_file_path  # Возвращаем путь к файлу для использования в тестах
    os.remove(test_file_path)  # Удаляем файл после теста


# Фикстура для создания пользовательских настроек
@pytest.fixture
def user_settings() -> Dict[str, Any]:
    """Возвращает тестовые пользовательские настройки."""
    return {"user_currencies": ["USD"], "user_stocks": []}


# Параметризация для тестирования различных сценариев транзакций
@pytest.mark.parametrize(
    "data, expected_expenses_total, expected_income_total",
    [
        (
            pd.DataFrame(
                {
                    "Дата операции": pd.to_datetime(["2023-10-01", "2023-10-02"]),
                    "Тип": ["Расход", "Расход"],
                    "Сумма": [100, 50],
                    "Категория": ["Еда", "Транспорт"],
                }
            ),
            150,
            0,
        ),
        (
            pd.DataFrame(
                {
                    "Дата операции": pd.to_datetime(["2023-10-01", "2023-10-02"]),
                    "Тип": ["Поступление", "Поступление"],
                    "Сумма": [200, 300],
                    "Категория": ["Зарплата", "Подарок"],
                }
            ),
            0,
            500,
        ),
        (
            pd.DataFrame(
                {
                    "Дата операции": pd.to_datetime(["2023-10-01", "2023-10-02", "2023-10-02"]),
                    "Тип": ["Расход", "Поступление", "Расход"],
                    "Сумма": [100, 200, 50],
                    "Категория": ["Еда", "Зарплата", "Наличные"],
                }
            ),
            150,
            200,
        ),
    ],
)
def test_process_transactions(
    data: pd.DataFrame, expected_expenses_total: int, expected_income_total: int, user_settings: Dict[str, Any]
) -> None:
    """Тестирование обработки различных сценариев транзакций."""

    result = process_transactions(data, "2023-10-02 00:00:00", "D", user_settings)

    assert result["expenses"]["total_amount"] == expected_expenses_total
    assert result["income"]["total_amount"] == expected_income_total


def test_read_excel_data(test_excel_file: str) -> None:
    """Тестирование чтения данных из Excel файла."""

    # Читаем данные из файла
    result = read_excel_data(test_excel_file)

    # Проверяем, что считанные данные совпадают с оригинальными
    expected_df = pd.DataFrame({"Column1": [1, 2], "Column2": [3, 4]})
    pd.testing.assert_frame_equal(result, expected_df)


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

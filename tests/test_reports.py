from typing import Any, Callable, Dict
from unittest import mock

import pandas as pd
import pytest

from src.reports import report_decorator, spending_by_category

# Пример данных для тестирования
transactions_data: pd.DataFrame = pd.DataFrame(
    {
        "Дата операции": [
            "10.01.2024 12:00:00",
            "15.01.2024 12:00:00",
            "10.02.2024 12:00:00",
            "20.02.2024 12:00:00",
            "01.03.2024 12:00:00",
        ],
        "Категория": ["Еда", "Транспорт", "Еда", "Развлечения", "Еда"],
        "Сумма операции": ["-100.50", "-50.00", "-200.75", "-150.25", "-300.00"],
    }
)

# Преобразуем даты в нужный формат
transactions_data["Дата операции"] = pd.to_datetime(transactions_data["Дата операции"], dayfirst=True)


@pytest.mark.parametrize(
    "category, date, expected_total",
    [
        ("Развлечения", "2024-02-15", 0.0),  # Нет расходов по категории Развлечения до указанной даты
        ("Транспорт", "2024-03-01", 50.0),  # Расходы по категории Транспорт до указанной даты
        ("Еда", "2024-02-15", 301.25),  # Расходы по категории Еда до указанной даты
    ],
)
def test_spending_by_category(mocker: Any, category: str, date: str, expected_total: float) -> None:
    """Тестирование функции spending_by_category с параметризацией."""

    # Мокаем метод logging.info для подавления вывода во время тестирования
    mocker.patch("logging.info")

    result = spending_by_category(transactions_data.copy(), category, date)  # Используем копию данных

    assert result["category"] == category
    assert result["total_spent"] == expected_total  # Проверяем общую сумму расходов


@pytest.mark.parametrize(
    "category, date",
    [
        ("Еда", "некорректная дата"),  # Проверка на некорректную дату
    ],
)
def test_spending_by_category_invalid_date(mocker: Any, category: str, date: str) -> None:
    """Тестирование функции spending_by_category при некорректной дате."""

    mocker.patch("logging.info")

    with pytest.raises(ValueError):
        spending_by_category(transactions_data.copy(), category, date)


@mock.patch("builtins.open", new_callable=mock.mock_open)
@mock.patch("src.reports.logging.info")
def test_report_decorator_success(
    mock_logging_info: Any, mock_open: mock.MagicMock, mock_function: Callable[[], Dict[str, str]]
) -> None:
    """Тест на успешное сохранение отчета в файл."""
    decorated_function = report_decorator(mock_function)
    result = decorated_function()

    # Проверяем, что функция вернула ожидаемый результат
    assert result == {"data": "test report"}

    # Получаем имя файла, который был вызван в open
    filename = mock_open.call_args[0][0]

    # Проверяем, что имя файла соответствует ожидаемому формату
    assert filename.startswith("spending_report_") and filename.endswith(".json")

    # Проверяем, что open был вызван с правильными параметрами
    mock_open.assert_called_once_with(filename, "w", encoding="utf-8")

    # Проверяем, что логирование произошло
    mock_logging_info.assert_called_once()

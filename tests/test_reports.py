from datetime import datetime, timedelta
from typing import Any, Callable, Dict
from unittest import mock

from src.reports import report_decorator, spending_by_category


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


def test_spending_by_category_with_transactions(transactions: Any) -> None:
    """Тест на наличие транзакций в указанной категории."""
    result: Dict[str, Any] = spending_by_category(transactions, category="Продукты")

    assert result["category"] == "Продукты"

    # Приводим к типу float для корректного сравнения
    assert float(result["total_spent"]) == 3500.75

    assert result["date_range"]["start_date"] == (datetime.now() - timedelta(days=90)).strftime("%d.%m.%Y")
    assert result["date_range"]["end_date"] == datetime.now().strftime("%d.%m.%Y")


def test_spending_by_category_no_transactions(transactions: Any) -> None:
    """Тест на отсутствие транзакций в указанной категории."""
    result: Dict[str, Any] = spending_by_category(transactions, category="Транспорт")

    assert result["category"] == "Транспорт"
    assert result["total_spent"] == 0.0
    assert result["date_range"]["start_date"] == (datetime.now() - timedelta(days=90)).strftime("%d.%m.%Y")
    assert result["date_range"]["end_date"] == datetime.now().strftime("%d.%m.%Y")


def test_spending_by_category_without_date(transactions: Any) -> None:
    """Тест на использование текущей даты при отсутствии переданной даты."""
    result: Dict[str, Any] = spending_by_category(transactions, category="Продукты")

    assert result["category"] == "Продукты"
    assert result["total_spent"] == 3500.75

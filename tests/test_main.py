import json
from typing import Any, Dict, Generator, List
from unittest.mock import MagicMock, patch

import pytest

from src.main import main


# Фикстура для имитации данных из Excel
@pytest.fixture
def mock_excel_data() -> List[Dict[str, int]]:
    return [{"id": 1, "amount": 100}]


# Фикстура для имитации настроек пользователя
@pytest.fixture
def mock_user_settings() -> Dict[str, str]:
    return {"currency": "USD"}


# Фикстура для имитации функции process_transactions
@pytest.fixture
def mock_process_transactions() -> Generator[MagicMock, None, None]:
    with patch("src.main.process_transactions") as mock:
        yield mock


# Параметризация теста с различными значениями даты и типа транзакции
@pytest.mark.parametrize(
    "input_date, period_input, expected_total",
    [
        ("2024-10-14 12:00:00", "M", {"total": 100, "currency": "USD"}),
        ("2024-10-15 12:00:00", "W", {"total": 200, "currency": "EUR"}),
    ],
)
@patch("src.main.read_excel_data")
@patch("src.main.get_user_settings")
@patch("builtins.input", side_effect=["2024-10-14 12:00:00", "M"])
@patch("builtins.print")
def test_main(
    mock_print: MagicMock,
    mock_input: MagicMock,
    mock_get_user_settings: MagicMock,
    mock_read_excel_data: MagicMock,
    mock_process_transactions: MagicMock,
    input_date: str,
    period_input: str,
    expected_total: Dict[str, Any],
    mock_excel_data: List[Dict[str, int]],
    mock_user_settings: Dict[str, str],
) -> None:
    # Настройка возвращаемых значений функций
    mock_read_excel_data.return_value = mock_excel_data
    mock_get_user_settings.return_value = mock_user_settings
    mock_process_transactions.return_value = expected_total

    # Вызов основной функции
    main()

    # Проверка вызовов моков
    mock_read_excel_data.assert_called_once_with("../data/operations.xls")
    mock_get_user_settings.assert_called_once_with("../user_settings.json")
    mock_process_transactions.assert_called_once_with(mock_excel_data, input_date, period_input, mock_user_settings)

    # Проверка корректности вывода в print
    expected_output = json.dumps(expected_total, ensure_ascii=False, indent=4)
    mock_print.assert_called_once_with(expected_output)


if __name__ == "__main__":
    pytest.main()

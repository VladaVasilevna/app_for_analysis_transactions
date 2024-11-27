from typing import Any, Dict, List, Optional
from unittest.mock import MagicMock, patch

import pandas as pd

from src.utils import get_currency_rates, get_stock_prices, read_excel_data


def test_read_excel_data(mock_excel_data: pd.DataFrame) -> None:
    with patch("pandas.read_excel", return_value=mock_excel_data):
        df: Optional[pd.DataFrame] = read_excel_data("mock_path.xlsx")
        assert df is not None  # Проверяем, что df не None
        assert df.shape[0] == 3  # Проверяем количество строк


@patch("src.utils.requests.get")
def test_get_currency_rates(mock_requests: MagicMock) -> None:
    mock_requests.return_value.status_code = 200
    mock_requests.return_value.json.return_value = {"rates": {"USD": 1.0, "EUR": 0.85}}

    rates: List[Dict[str, Any]] = get_currency_rates(["USD", "EUR"])

    assert len(rates) == 2
    assert rates[0]["currency"] == "USD"
    assert rates[1]["currency"] == "EUR"


@patch("src.utils.requests.get")
def test_get_stock_prices(mock_requests: MagicMock) -> None:
    mock_requests.return_value.status_code = 200
    mock_requests.return_value.json.return_value = {"data": [{"last": 150}]}

    prices: List[Dict[str, Any]] = get_stock_prices(["AAPL"])

    assert len(prices) == 1
    assert prices[0]["stock"] == "AAPL"

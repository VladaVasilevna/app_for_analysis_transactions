from typing import Any, Dict
from unittest.mock import patch

import pandas as pd

from src.views import generate_response


def test_generate_response(mock_excel_data: pd.DataFrame, user_settings: Dict[str, Any]) -> None:
    with patch("src.views.read_excel_data", return_value=mock_excel_data):
        response: Dict[str, Any] = generate_response("2024-01-15 12:00:00", user_settings)

        assert response["greeting"] == "Добрый день"
        assert len(response["cards"]) == 1
        assert len(response["top_transactions"]) == 1

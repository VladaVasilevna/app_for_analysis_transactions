import json
import unittest
from unittest.mock import MagicMock, patch

from src.main import main


class TestMainFunction(unittest.TestCase):

    @patch("src.main.read_excel_data")
    @patch("src.main.get_user_settings")
    @patch("src.main.process_transactions")
    @patch("builtins.input", side_effect=["2024-10-14 12:00:00", "M"])
    @patch("builtins.print")
    def test_main(
        self,
        mock_print: MagicMock,
        mock_input: MagicMock,  # Исправление: добавлен аргумент для замокированного ввода
        mock_process_transactions: MagicMock,
        mock_get_user_settings: MagicMock,
        mock_read_excel_data: MagicMock,
    ) -> None:
        # Настройка возвращаемых значений функций
        mock_read_excel_data.return_value = [{"id": 1, "amount": 100}]
        mock_get_user_settings.return_value = {"currency": "USD"}
        mock_process_transactions.return_value = {"total": 100, "currency": "USD"}

        # Вызов основной функции
        main()

        # Проверка вызовов моков
        mock_read_excel_data.assert_called_once_with("../data/operations.xls")
        mock_get_user_settings.assert_called_once_with("../user_settings.json")
        mock_process_transactions.assert_called_once_with(
            [{"id": 1, "amount": 100}], "2024-10-14 12:00:00", "M", {"currency": "USD"}
        )

        # Проверка корректности вывода в print
        expected_output: str = json.dumps({"total": 100, "currency": "USD"}, ensure_ascii=False, indent=4)
        mock_print.assert_called_once_with(expected_output)


if __name__ == "__main__":
    unittest.main()

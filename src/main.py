import json
from typing import Any, Dict

from utils import get_user_settings, process_transactions, read_excel_data


def main() -> None:
    """Основная функция для запуска приложения."""
    transactions_file_path = "../data/operations.xls"
    user_settings_path = "../user_settings.json"

    # Чтение данных
    transactions_data = read_excel_data(transactions_file_path)

    # Получение пользовательских настроек
    user_settings = get_user_settings(user_settings_path)

    # Ввод даты и времени
    input_datetime = input("Введите дату и время (YYYY-MM-DD HH:MM:SS): ")

    # Ввод периода (по умолчанию месяц)
    period_input = input("Введите период (W/M/Y/ALL): ") or "M"

    # Обработка транзакций и вывод результата в формате JSON
    result_json: Dict[str, Any] = process_transactions(transactions_data, input_datetime, period_input, user_settings)

    print(json.dumps(result_json, ensure_ascii=False, indent=4))


if __name__ == "__main__":
    main()

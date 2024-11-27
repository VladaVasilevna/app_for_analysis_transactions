import json
from typing import Any, Dict

from dotenv import load_dotenv

from src.services import investment_bank
from src.utils import read_excel_data
from src.views import generate_response

# Загрузка переменных окружения из файла .env
load_dotenv()


def main() -> None:
    """Основная функция для запуска приложения."""
    transactions_file_path: str = "../data/operations.xlsx"
    user_settings_path: str = "../user_settings.json"

    # Чтение данных
    transactions_data = read_excel_data(transactions_file_path)

    if transactions_data is None:
        print("Не удалось загрузить данные о транзакциях.")
        return

    # Получение пользовательских настроек
    with open(user_settings_path, "r", encoding="utf-8") as f:
        user_settings: Dict[str, Any] = json.load(f)

    # Ввод даты и времени
    input_datetime: str = input("Введите дату и время (YYYY-MM-DD HH:MM:SS): ")

    # Обработка транзакций и вывод результата в формате JSON
    result_json: Dict[str, Any] = generate_response(input_datetime, user_settings)

    # Печать результата с отступами для удобства чтения
    print(json.dumps(result_json, ensure_ascii=False, indent=4))

    # Ввод месяца и лимита округления для Инвесткопилки
    input_month: str = input("Введите месяц для расчета (YYYY-MM): ")
    limit: int = int(input("Введите лимит округления (10, 50 или 100): "))

    # Проверка на допустимый лимит
    if limit not in [10, 50, 100]:
        print("Недопустимый лимит. Пожалуйста, выберите 10, 50 или 100.")
        return

    # Преобразование данных о транзакциях в список словарей
    transactions = []
    for index, row in transactions_data.iterrows():
        transactions.append(
            {
                "Дата операции": row["Дата операции"],  # Используем строку напрямую
                "Сумма операции": row["Сумма операции с округлением"],
            }
        )

    # Вычисление суммы отложенной в 'Инвесткопилку'
    saved_amount = investment_bank(input_month, transactions, limit)

    # Печать результата отложенной суммы
    print(f"Сумма отложенная в 'Инвесткопилку' за {input_month}: {saved_amount:.2f} ₽")


if __name__ == "__main__":
    main()

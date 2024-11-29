import json
from datetime import datetime
from typing import Any, Dict, Optional

from dotenv import load_dotenv

from src.reports import spending_by_category
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
    while True:
        input_datetime: str = input("Введите дату и время (YYYY-MM-DD HH:MM:SS): ")
        try:
            # Проверка формата даты и времени
            datetime.strptime(input_datetime, "%Y-%m-%d %H:%M:%S")
            break  # Выход из цикла, если ввод корректен
        except ValueError:
            print("Некорректный формат даты и времени. Пожалуйста, попробуйте снова.")

    # Обработка транзакций и вывод результата в формате JSON
    result_json: Dict[str, Any] = generate_response(input_datetime, user_settings)

    print(json.dumps(result_json, ensure_ascii=False, indent=4))

    # Ввод месяца и лимита округления для Инвесткопилки
    while True:
        input_month: str = input("Введите месяц для расчета (YYYY-MM): ")
        try:
            # Проверка формата месяца
            datetime.strptime(input_month, "%Y-%m")
            break
        except ValueError:
            print("Некорректный формат месяца. Пожалуйста, используйте формат YYYY-MM.")

    # Проверка на допустимый лимит
    while True:
        try:
            limit: int = int(input("Введите лимит округления (10, 50 или 100): "))

            if limit in [10, 50, 100]:
                break
            else:
                print("Недопустимый лимит. Пожалуйста, выберите 10, 50 или 100.")
        except ValueError:
            print("Недопустимый лимит. Пожалуйста, выберите 10, 50 или 100.")

    # Преобразование данных о транзакциях в список словарей
    transactions = []
    for index, row in transactions_data.iterrows():
        transactions.append(
            {
                "Дата операции": row["Дата операции"],
                "Сумма операции": row["Сумма операции"],
            }
        )

    # Вычисление суммы отложенной в 'Инвесткопилку'
    saved_amount = investment_bank(input_month, transactions, limit)

    # Печать результата отложенной суммы
    print(f"Сумма отложенная в 'Инвесткопилку' за {input_month}: {saved_amount:.2f} ₽")

    # Получение отчета по категориям
    while True:
        category: str = input("Введите категорию для анализа расходов: ").strip()

        # Проверка, что категория не пустая
        if not category:
            print("Категория не может быть пустой. Пожалуйста, введите корректную категорию.")
            continue

        # Проверка, существует ли категория в данных транзакций
        if category not in transactions_data["Категория"].unique():
            print(f"Категория '{category}' не найдена. Пожалуйста, введите существующую категорию.")
        else:
            break

    # Ввод даты для анализа расходов
    while True:
        input_date: Optional[str] = input(
            "Введите дату для анализа расходов (YYYY-MM-DD), или нажмите Enter для текущей даты: "
        )
        # Если дата не введена, используем текущую дату
        if not input_date.strip():
            input_date = None
            break

        try:
            # Проверка формата даты
            datetime.strptime(input_date, "%Y-%m-%d")
            break
        except ValueError:
            print("Некорректный формат даты. Пожалуйста, используйте формат YYYY-MM-DD.")

    try:

        report = spending_by_category(transactions_data, category, input_date)
        print(json.dumps(report, ensure_ascii=False, indent=4))
    except Exception as e:
        print(f"Ошибка при получении отчета по категории '{category}': {e}")


if __name__ == "__main__":
    main()

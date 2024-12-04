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

    print(
        """Страница 'Главная'
Получить данные с начала месяца, на который выпадает входящая дата, по входящую дату.\n"""
    )

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

    print(
        """\n'Инвесткопилка'
Позволяет копить через округление ваших трат.
Чем активнее расплачиваетесь картой, тем быстрее копятся деньги в копилке.\n"""
    )

    while True:
        try:
            limit: int = int(input("Введите порог округления (10, 50 или 100): "))

            if limit in [10, 50, 100]:
                break
            else:
                print("Недопустимый порог. Пожалуйста, выберите 10, 50 или 100.")
        except ValueError:
            print("Недопустимый порог. Пожалуйста, выберите 10, 50 или 100.")

    while True:
        # Ввод даты для расчета Инвесткопилки
        input_month: str = input("Введите дату для расчета отложенной суммы (YYYY-MM): ")
        try:
            # Проверка формата даты
            datetime.strptime(input_month, "%Y-%m")

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

            if saved_amount is None:
                print("Дата не найдена. Введите другую дату.")
                continue

            # Печать результата отложенной суммы
            print(f"Сумма отложенная в 'Инвесткопилку' за {input_month}: {saved_amount:.2f} ₽")
            break

        except ValueError:
            print("Некорректный формат даты. Пожалуйста, используйте формат YYYY-MM.")

    print(
        """\n'Траты по категории'
Получить данные о тратах по заданной категории за последние три месяца (от переданной даты).\n"""
    )
    # Получение отчета по категориям
    original_category = None
    while True:
        category_input: str = input("Введите категорию для анализа расходов: ").strip()  # Вводим категорию
        category_lower = category_input.lower()  # Преобразуем введённое значение в нижний регистр

        # Проверка, что категория не пустая
        if not category_input:
            print("Категория не может быть пустой. Пожалуйста, введите корректную категорию.")
            continue

        # Поиск категории в данных транзакций независимо от регистра
        matching_categories = transactions_data["Категория"].str.lower()  # Преобразуем все категории в нижний регистр
        if category_lower not in matching_categories.unique():
            print(f"Категория '{category_input}' не найдена. Пожалуйста, введите существующую категорию.")
        else:
            # Получаем оригинальное название категории для вывода
            original_category = transactions_data.loc[
                matching_categories[matching_categories == category_lower].index[0], "Категория"
            ]
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
        report = spending_by_category(transactions_data, original_category, input_date)
        print(json.dumps(report, ensure_ascii=False, indent=4))
    except Exception as e:
        print(f"Ошибка при получении отчета по категории '{original_category}': {e}")


if __name__ == "__main__":
    main()

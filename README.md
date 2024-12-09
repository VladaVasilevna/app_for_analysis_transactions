# Банковское приложение

## Описание:

Приложение для анализа транзакций, которые находятся в Excel-файле. Приложение генерирует JSON-данные для веб-страниц.
Реализованы следующие примеры страниц:
Веб-страницы: Главная
Сервисы: Инвесткопилка
Отчеты: Траты по категории

## Работа функций:

1. main - основная функция для запуска приложения.
2. generate_response - функция формирования JSON ответа.
3. read_excel_data - функция чтения данных из Excel файла.
4. get_currency_rates - функция получения курсов валют с API.
5. get_stock_prices - функция получения цен акций из API.
6. investment_bank - функция вычисления суммы, отложенной в 'Инвесткопилку' за указанный месяц.
7. report_decorator - декоратор для записи отчета в файл с названием по умолчанию.
8. spending_by_category - функция возвращает траты по заданной категории за последние три месяца от заданной даты.

## Требования к окружению:

   - Установите:

     ```Python 3.8+```

## Установка проекта:

- Склонировать репозиторий:

       ```bash git clone https://github.com/VladaVasilevna/app_for_analysis_transactions```

- Перейти в директорию проекта:

       ```bash cd ваш-проект```

- (Если требуется) Создать и активировать виртуальное окружение:

  ```bash python -m venv venv source venv/bin/activate  # или venv\Scripts\activate для Windows```

- Склонировать репозиторий:

       ```bash git clone https://github.com/VladaVasilevna/app_for_analysis_transactions```

- Перейти в директорию проекта:

       ```bash cd ваш-проект```

- (Если требуется) Создать и активировать виртуальное окружение:

       ```bash python -m venv venv source venv/bin/activate  # или venv\Scripts\activate для Windows```

## Установка зависимостей:

     ```bash pip install -r requirements.txt```



## Как запустить проект:

     ```bash python manage.py runserver```

## Тестирование
- Для всех фунцкций в проекте написаны тесты.
- Использованы фикстуры для создания необходимых входных данных для тестов.
- Использована параметризация в тестах для обеспечения тестирования функциональности с различными входными данными.
- Использованы Mock и patch.
- Создан отчет HTML.

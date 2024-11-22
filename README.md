# Веб-страницы

## Описание:

Приложение для анализа транзакций, которые находятся в Excel-файле. Приложение генерирует JSON-данные для веб-страниц.

## Работа функций:

1. main - основная функция для запуска приложения.
2. generate_greeting - функция генерации приветствия в зависимости от времени суток.
3. prepare_response - функция формирования JSON ответа.
4. read_excel_data - функция чтения данных из Excel файла.
5. get_user_settings - функция получения пользовательских настроек из JSON файла.
6. fetch_currency_rates - функция получения курсов валют с API.
7. fetch_stock_prices - функция получения цен акций из API.
8. process_transactions - функция обработки транзакций и генерация JSON ответа.

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

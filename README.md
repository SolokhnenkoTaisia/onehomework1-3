# PythonProject2

## Описание проекта

PythonProject2 — учебный проект для работы с банковскими операциями клиента.

В проекте реализованы функции для маскирования данных банковских карт и счетов, а также функции для обработки списка банковских операций.

## Установка

1. Клонируйте репозиторий:

```bash
git clone https://github.com/SolokhnenkoTaisia/onehomework1-3.git
```

2. Перейдите в директорию проекта:

```bash
cd PythonProject2
```

3. Установите зависимости с помощью Poetry:

```bash
poetry install
```

## Использование

### Функция filter_by_state

Функция `filter_by_state` фильтрует список банковских операций по значению ключа `state`.

По умолчанию используется значение `EXECUTED`.

Пример:

```python
from src.processing import filter_by_state

operations = [
    {"id": 1, "state": "EXECUTED"},
    {"id": 2, "state": "CANCELED"},
    {"id": 3, "state": "EXECUTED"},
]

result = filter_by_state(operations)

print(result)
```

Результат:

```text
[
    {"id": 1, "state": "EXECUTED"},
    {"id": 3, "state": "EXECUTED"}
]
```

Можно указать другое значение `state`:

```python
result = filter_by_state(operations, "CANCELED")
```

### Функция sort_by_date

Функция `sort_by_date` сортирует список банковских операций по ключу `date`.

По умолчанию операции сортируются по убыванию даты.

Пример:

```python
from src.processing import sort_by_date

operations = [
    {"date": "2024-01-15"},
    {"date": "2024-03-20"},
    {"date": "2024-02-10"},
]

result = sort_by_date(operations)

print(result)
```

Для сортировки по возрастанию можно передать `reverse=False`:

```python
result = sort_by_date(operations, reverse=False)
```

## Тестирование

Для запуска тестов используйте команду:

```bash
poetry run pytest
```

В проекте используются параметризованные тесты и фикстуры для проверки различных вариантов работы функций.

Для проверки покрытия кода тестами и создания HTML-отчёта используйте:

```bash
poetry run pytest --cov=src --cov-report=term-missing --cov-report=html
```

Текущее покрытие кода тестами составляет 100%.

HTML-отчёт создаётся в папке `htmlcov/`. Для просмотра отчёта откройте файл `htmlcov/index.html` в браузере.

## Структура проекта

* `src/masks.py` — функции для маскирования номеров карт и счетов.
* `src/widget.py` — функции обработки данных банковских операций.
* `src/processing.py` — функции фильтрации и сортировки банковских операций.
* `tests/` — тесты проекта.
* `htmlcov/` — HTML-отчёт о покрытии кода тестами.


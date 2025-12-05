# PEP Parser

Парсер на **Scrapy** для сбора информации о всех [Python Enhancement Proposals (PEP)](https://peps.python.org/).

## Описание

Парсер выполняет следующие задачи:

1. Переходит на стартовую страницу [https://peps.python.org/numerical/](https://peps.python.org/numerical/) и собирает ссылки на все PEP.
2. Переходит на страницу каждого PEP и извлекает:
   - номер,
   - название,
   - статус.
3. Сохраняет данные в два CSV-файла в директорию `results/`:
   - **`pep_dateTtime.csv`** — полный список всех PEP с колонками: `number`, `name`, `status`.
   - **`status_summary_date_time.csv`** — сводка по статусам: `status`, `count`, а также итоговая строка `Total`.

## Структура проекта

```
scrapy_parser_pep/
├── pep_parse/              # Основной пакет Scrapy
│   ├── spiders/
│   │   └── pep.py          # Паук для сбора PEP
│   ├── items.py            # Определение элемента PepParseItem
│   ├── pipelines.py        # Пайплайн для агрегации статусов
│   └── settings.py         # Настройки Scrapy
├── results/                # Директория для сохранения результатов (создаётся автоматически)
├── requirements.txt        # Зависимости
├── scrapy.cfg              # Конфигурация Scrapy
└── README.md
```

## Технологии

- Python 3.9
- Scrapy

## Установка

1. Клонируйте репозиторий:
    ```bash
    git clone <ваш-репозиторий>
    cd scrapy_parser_pep
    ```
2. Создайте и активируйте виртуальное окружение:
    ```bash
    python -m venv venv
    # Windows
    venv\Scripts\activate
    # Linux/macOS
    source venv/bin/activate
    ```
3. Установите зависимости:
    ```bash
    pip install -r requirements.txt
    ```

## Запуск

Запустите паука командой:
```bash
scrapy crawl pep
```

После завершения в корне проекта появится папка `results/` с двумя CSV-файлами.

## Формат выходных файлов

`pep_ГГГГ-ММ-ДД<T>ЧЧ-ММ-СС.csv`

Пример:
```
number,name,status
1,PEP Purpose and Guidelines,Active
218,Adding a Built-In Set Object Type,Final
...
```

`status_summary_ГГГГ-ММ-ДД_ЧЧ-ММ-СС.csv`

Пример:
```
status,count
Accepted,20
Active,35
...
Total,706
```

## Автор

Илья Горбачев

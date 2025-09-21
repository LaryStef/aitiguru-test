# Тестовое задание

### Задание 1 в файле task1.sql

### Задание 2 в файле task2.sql

## Запуск проекта

### Подготовка окружения

1. **Установка uv:**
```bash
pip install uv
```

2. **Создание виртуального окружения:**
```bash
uv venv
source .venv/bin/activate
```

3. **Установка зависимостей:**
```bash
uv sync
```

4. **Настройка URL базы данных в app/core/config.py:**
```bash
"DATABASE_URL=postgresql://username:password@localhost/dbname"
```

### Запуск сервиса

```bash
uvicorn app.main:app
```

Сервис будет доступен по адресу: http://localhost:8000

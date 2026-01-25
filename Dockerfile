# Базовый образ Python
FROM python:3.11-slim-buster

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем требования
COPY requirements.txt .

# Установка зависимостей
RUN pip install --no-cache-dir -r requirements.txt

# Копируем весь исходный код
COPY . .

# Запуск FastAPI с помощью Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]



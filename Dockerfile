FROM python:3.11-slim-bullseye

# Устанавливаем более безопасные настройки
RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Установка зависимостей
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копирование кода приложения
COPY . .

# Открытие порта
EXPOSE 8000

# Команда для запуска приложения с HTTPS
CMD ["python", "-m", "app.main"]

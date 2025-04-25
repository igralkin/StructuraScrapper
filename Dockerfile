# Базовый минимальный образ
FROM python:3.10-slim

# Устанавливаем рабочую директорию
WORKDIR /app

# Устанавливаем зависимости
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем весь проект
COPY . .

# По умолчанию запускаем main.py с возможностью передать аргументы
ENTRYPOINT ["python", "main.py"]
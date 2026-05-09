# Stage 1: Сборка зависимостей
FROM python:3.11-slim AS builder

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# Stage 2: Финальный образ
FROM python:3.11-slim

WORKDIR /app

# Копируем установленные пакеты из builder
COPY --from=builder /root/.local /root/.local

# Копируем код приложения
COPY app/ ./app/
COPY app/templates/ ./app/templates/

# Добавляем путь к пакетам в PATH
ENV PATH=/root/.local/bin:$PATH

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

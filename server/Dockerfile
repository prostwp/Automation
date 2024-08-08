FROM python:3.12-slim

# Устанавливаем рабочую директорию
WORKDIR /usr/app/server

# Обновляем репозитории и устанавливаем необходимые пакеты
RUN apt-get update && apt-get install -y \
    python3-pip \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*
# Копируем файлы с зависимостями
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt



# Копируем остальные файлы сервера
COPY . .

# Запускаем сервер
CMD ["python", "server.py"]
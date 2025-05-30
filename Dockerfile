# Dockerfile

# Используем официальный образ Python.
# Выбираем версию Python 3.10, так как это рекомендовано для последних версий Django.
# Образ 'slim-buster' или 'slim-bullseye' - это облегченные версии, что хорошо для продакшена.
FROM python:3.10-slim-buster

# Устанавливаем системные зависимости, необходимые для mysqlclient и других пакетов.
# 'build-essential' для компиляции, 'libmysqlclient-dev' для MySQL.
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        build-essential \
        libmariadb-dev-compat \
        pkg-config \
    && rm -rf /var/lib/apt/lists/*

# Устанавливаем рабочую директорию внутри контейнера
WORKDIR /app

# Копируем файл requirements.txt в рабочую директорию
COPY requirements.txt /app/

# Устанавливаем Python-зависимости из requirements.txt
# Используем --no-cache-dir для экономии места в образе
RUN pip install --no-cache-dir -r requirements.txt

# Копируем остальной код приложения в рабочую директорию
COPY . /app/

# Собираем статические файлы Django
# Эту команду нужно выполнить в контейнере, чтобы статика была доступна.
# CMD [ "python", "manage.py", "collectstatic", "--noinput" ]
# Примечание: collectstatic будем выполнять один раз при сборке, чтобы статика была сразу в образе.
# Это упрощает настройку Nginx/веб-сервера на хостинге.
RUN python manage.py collectstatic --noinput

# Открываем порт, который будет слушать Gunicorn (или другой WSGI-сервер)
# Обычно для веб-приложений это 8000 или 80.
EXPOSE 8000

# Определение команды, которая будет запускаться при старте контейнера
# Используем Gunicorn для запуска Django WSGI-приложения.
# tomi_ai_service.wsgi:application -> это путь к твоему WSGI-файлу и переменной 'application'.
# --bind 0.0.0.0:8000 -> Gunicorn будет слушать запросы на всех интерфейсах на порту 8000.
# --workers 3 -> Количество рабочих процессов Gunicorn (можно настроить в зависимости от ресурсов).
# --timeout 120 -> Таймаут для запросов.
CMD ["gunicorn", "tomi_ai_service.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "3", "--timeout", "120"]
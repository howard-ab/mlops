# Используем python:3.10-slim как указано в задании
FROM python:3.10-slim

# Установка системных зависимостей для сборки
RUN apt-get update && apt-get install -y \
    g++ \
    cmake \
    make \
    git \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Копируем все файлы проекта
COPY . .

# Устанавливаем Python зависимости для сборки
RUN pip install --no-cache-dir \
    build \
    pybind11 \
    scikit-build-core

# Собираем wheel пакет
RUN python -m build --wheel

# Находим и копируем wheel файл
RUN find dist -name "*.whl" -exec cp {} /app/myalgo.whl \;

# Устанавливаем наш пакет
RUN pip install --no-cache-dir /app/myalgo.whl

# Проверяем, что пакет установился
RUN python -c "import myalgo; print('Package imported successfully!')"

# Сохраняем wheel файл для проверки
RUN cp /app/myalgo.whl /app/myalgo_package.whl

# Команда по умолчанию - запуск тестов
CMD ["python", "test_myalgo.py"]
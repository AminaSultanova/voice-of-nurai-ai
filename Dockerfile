FROM python:3.11-slim

WORKDIR /app

# Устанавливаем системные зависимости
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Копируем зависимости
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем весь код
COPY . .

# Создаём папку для ChromaDB
RUN mkdir -p /app/chroma_db

# Загружаем статьи в базу знаний (при сборке)
RUN python -c "from knowledge_base import load_articles_from_folder; load_articles_from_folder()"

# Запускаем бота
CMD ["python", "bot.py"]
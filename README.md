# Voice of Nurai — AI Safety Assistant

Telegram-бот для помощи девушкам в опасных ситуациях. Работает на основе RAG (Retrieval-Augmented Generation) с базой знаний из проверенных статей по безопасности.

## Технологии

- Python 3.11
- Telegram Bot API
- OpenRouter (Gemini 2.0 Flash)
- ChromaDB + sentence-transformers (RAG)
- Docker

## Структура проекта

voice-of-nurai-ai/
├── bot.py              # Основной Telegram бот
├── ai_assistant.py     # AI логика + OpenRouter API
├── knowledge_base.py   # RAG + ChromaDB (векторный поиск)
├── data/               # Папка со статьями (база знаний)
├── Dockerfile          # Для деплоя на Railway
├── requirements.txt    # Зависимости
├── .env.example        # Пример переменных окружения
└── README.md           # Документация

## Локальный запуск

### 1. Клонировать репозиторий

git clone https://github.com/your-org/voice-of-nurai-ai.git
cd voice-of-nurai-ai

### 2. Установить зависимости

pip install -r requirements.txt

### 3. Создать файл .env с токенами

TELEGRAM_BOT_TOKEN=your_telegram_bot_token
OPENROUTER_API_KEY=your_openrouter_api_key

Где взять:
- TELEGRAM_BOT_TOKEN — у @BotFather в Telegram
- OPENROUTER_API_KEY — на openrouter.ai/keys
Обратитесь ко мне за этой информацией.

### 4. Загрузить статьи в базу знаний (ChromaDB)

python knowledge_base.py

При первом запуске создастся папка chroma_db/ с векторными индексами статей из папки data/.

### 5. Запустить бота

python bot.py

Бот запустится и будет отвечать на сообщения в Telegram.

---

## Деплой на Railway (инструкция для DevSecOps)

### 1. Подготовка репозитория

Репозиторий уже содержит:
- Dockerfile — для сборки образа
- requirements.txt — все зависимости
- knowledge_base.py — предзагрузка статей при сборке

### 2. Подключение репозитория к Railway

1. Зайти в Railway.app
2. Нажать New Project → Deploy from GitHub repo
3. Выбрать репозиторий voice-of-nurai-ai
4. Railway автоматически обнаружит Dockerfile

### 3. Переменные окружения

В Railway добавить следующие переменные:

| Variable | Description |
| TELEGRAM_BOT_TOKEN | Токен Telegram бота |
| OPENROUTER_API_KEY | API ключ OpenRouter |

### 4. Настройки деплоя

- Builder: Dockerfile (автоопределение)
- Root directory: / (корень репозитория)
- Start command: не нужна (указана в Dockerfile CMD ["python", "bot.py"])

### 5. Деплой

Нажать Deploy. Railway:
1. Соберёт Docker образ
2. Установит зависимости
3. Загрузит статьи в ChromaDB (выполнится knowledge_base.py)
4. Запустит bot.py

### 6. Проверка после деплоя

После успешного деплоя:
1. Открыть Telegram
2. Найти бота по username (указан при создании через BotFather)
3. Отправить команду /start
4. Бот должен ответить приветствием

### 7. Health check (опционально)

Если нужен health check для Railway, добавить в bot.py:

from flask import Flask
import threading

app = Flask(__name__)

@app.route('/health')
def health():
    return 'OK', 200

# Запуск health check сервера в отдельном потоке
threading.Thread(target=lambda: app.run(port=8080, host='0.0.0.0'), daemon=True).start()

После этого Railway сможет проверять статус бота через порт 8080.

---

## Troubleshooting

### Бот не отвечает после деплоя

1. Проверить логи Railway:
   railway logs

2. Проверить переменные окружения:
   - Убедиться, что TELEGRAM_BOT_TOKEN и OPENROUTER_API_KEY переданы
   - Проверить, нет ли лишних пробелов или кавычек

3. Проверить ChromaDB:
   - В логах должно быть: "Загружено X фрагментов из 5 статей"
   - Если папка chroma_db не создалась — проверить права на запись

4. Перезапустить деплой:
   - Нажать Redeploy в Railway

### Ошибка при сборке Docker

- Проверить, что все файлы закоммичены в GitHub
- Убедиться, что requirements.txt актуален

### Бот запускается, но не отвечает на русском

- Бот адаптирован для Кыргызстана и СНГ
- Экстренный номер: 112
- Если вопрос на английском — бот должен отвечать на английском

---

## Переменные окружения (полный список)

| Variable | Required | Description |
|----------|----------|-------------|
| TELEGRAM_BOT_TOKEN | Да | Токен от BotFather |
| OPENROUTER_API_KEY | Да | API ключ OpenRouter |


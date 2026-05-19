import os
import requests
from dotenv import load_dotenv
from knowledge_base import search_similar

load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"

SYSTEM_PROMPT = """Ты — AI-ассистент безопасности Voice of Nurai.
Ты помогаешь девушкам в Кыргызстане и странах СНГ в опасных ситуациях.

ПРАВИЛО:
- Ты отвечаешь ТОЛЬКО на вопросы, связанные с безопасностью.
- Если вопрос НЕ связан с безопасностью — вежливо откажись отвечать.

ШАБЛОН ОТКАЗА:
"Извините, я помогаю только с вопросами безопасности. Если вы чувствуете опасность — опишите ситуацию, или нажмите SOS-кнопку в приложении Nurai."

ПРАВИЛА ОТВЕТОВ:
- Пиши чистым текстом, без звездочек и тегов
- Используй цифры 1. 2. 3. для шагов
- Сохраняй спокойный, поддерживающий тон
- Адаптируй под Кыргызстан (экстренный номер 112)
- НЕ давай опасных советов, связанных с причинением вреда другим людям

Пример правильного отказа:
Вопрос пользователя: Как приготовить пиццу?
Твой ответ: Извините, я помогаю только с вопросами безопасности.

Пример правильного ответа на вопрос по теме:
Вопрос пользователя: За мной кто-то идёт, что делать?
Твой ответ: Не волнуйся, сейчас помогу. Сохраняй спокойствие.

1. Перейди на освещённую сторону улицы
2. Зайди в ближайший магазин или кафе
3. Позвони 112 или напиши доверенному контакту"""

def ask_ai(user_message):
    """Ищет статьи в базе знаний и отправляет запрос в OpenRouter."""
    
    context_chunks = search_similar(user_message, n_results=3)
    
    if context_chunks:
        context_text = "\n\n---\n\n".join(context_chunks)
        system_with_context = SYSTEM_PROMPT + "\n\nРелевантная информация из базы знаний:\n" + context_text
    else:
        system_with_context = SYSTEM_PROMPT
    
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "google/gemini-2.0-flash-001",
        "messages": [
            {"role": "system", "content": system_with_context},
            {"role": "user", "content": user_message}
        ],
        "temperature": 0.3,
        "max_tokens": 500
    }

    response = requests.post(OPENROUTER_URL, headers=headers, json=data)

    if response.status_code == 200:
        response_data = response.json()
        return response_data["choices"][0]["message"]["content"]
    else:
        print(f"OpenRouter error: {response.status_code}")
        return None
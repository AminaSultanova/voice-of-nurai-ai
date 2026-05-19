import os
import requests
from dotenv import load_dotenv
from knowledge_base import search_similar

load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"

SYSTEM_PROMPT = """Ты — AI-ассистент безопасности Voice of Nurai.
Ты помогаешь девушкам в Кыргызстане и странах СНГ в опасных ситуациях.

ПРАВИЛА:
- Отвечай на языке на котором пишет пользователь.
- Давай конкретные инструкции по шагам.
- Адаптируй советы под Кыргызстан и СНГ:
  - Экстренный номер: 112.
  - Вместо зарубежных сервисов предлагай местные решения.
- НЕ давай опасных советов (насилие, оружие, нарушение закона).
- Если не уверена в совете — предложи нажать SOS-кнопку или позвонить 112.
- Будь спокойной и поддерживающей.
- В опасных ситуациях сначала дай быстрые действия.
- Используй короткие пункты, не более 5-6."""

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
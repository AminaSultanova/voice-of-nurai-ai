import os
import requests
from dotenv import load_dotenv
from knowledge_base import search_similar

load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"

SYSTEM_PROMPT = """Ты — AI-ассистент безопасности Voice of Nurai.
Ты помогаешь девушкам в Кыргызстане и странах СНГ в опасных ситуациях.

ПРАВИЛА ОТВЕТОВ:
- Пиши чистым текстом, БЕЗ markdown и БЕЗ HTML-тегов (не используй **, *, <b>, </b> и т.д.)
- Пиши короткими пунктами, каждый с новой строки, используй цифры 1. 2. 3.
- Сохраняй спокойный, уверенный, поддерживающий тон
- Обращайся на "ты"
- Будь конкретной: давай действия, а не общие фразы
- Адаптируй под Кыргызстан и СНГ: экстренный номер 112

ПРИМЕР ХОРОШЕГО ОТВЕТА (на вопрос "что делать, если преследуют ночью"):
Не волнуйся, сейчас помогу. Главное — сохраняй спокойствие.

1. Не паникуй, но и не показывай страх. Иди уверенно, но будь начеку.

2. Перейди на освещённую улицу или туда, где есть люди. Избегай тёмных переулков и парков.

3. Позвони подруге или родственнику и попроси, чтобы с тобой поговорили по телефону, пока ты не дойдёшь до дома.

4. Если преследователь не отстаёт, зайди в ближайший магазин, кафе или любое людное место и попроси о помощи.

5. Если чувствуешь реальную угрозу, звони в милицию по номеру 112.

Помни, что твоя безопасность — самое главное. Если есть возможность, нажми кнопку SOS в приложении.

ОСТАЛЬНЫЕ ПРАВИЛА:
- Отвечай на языке пользователя
- НЕ давай опасных советов (насилие, оружие)
- Если не уверена — предложи нажать SOS или позвонить 112"""

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
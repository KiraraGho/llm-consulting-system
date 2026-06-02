from httpx import AsyncClient, HTTPError

from app.core.config import settings


async def ask_openrouter(prompt: str) -> str:
    """Отправляет запрос пользователя в OpenRouter и возвращает ответ LLM"""
    url = f"{settings.openrouter_base_url}/chat/completions"

    headers = {
        "Authorization": f"Bearer {settings.openrouter_api_key}",
        "HTTP-Referer": settings.openrouter_site_url,
        "X-Title": settings.openrouter_app_name,
        "Content-Type": "application/json",
    }

    payload = {
        "model": settings.openrouter_model,
        "messages": [
            {
                "role": "user",
                "content": prompt,
            }
        ],
    }

    try:
        async with AsyncClient(timeout=60.0) as client:
            response = await client.post(url, headers=headers, json=payload)

        if response.status_code >= 400:
            return f"Ошибка OpenRouter {response.status_code}: {response.text}"

        data = response.json()
        return data["choices"][0]["message"]["content"]

    except (HTTPError, KeyError, IndexError) as exc:
        return f"Ошибка при обращении к LLM: {exc}"
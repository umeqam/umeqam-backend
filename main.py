from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from openai import OpenAI
import os

app = FastAPI(title="UMEQAM Dream Analyzer")

client = OpenAI(
    api_key=os.getenv("XAI_API_KEY"),
    base_url="https://api.x.ai/v1"
)

class DreamRequest(BaseModel):
    dream_text: str

@app.post("/analyze-dream")
async def analyze_dream(request: DreamRequest):
    if not request.dream_text.strip():
        raise HTTPException(status_code=400, detail="Описание сна не может быть пустым")

    dream = request.dream_text

    # Один общий анализ от Grok (быстро и качественно)
    try:
        response = client.chat.completions.create(
            model="grok-4-1-fast-reasoning",
            messages=[{
                "role": "user",
                "content": f"Проанализируй сон: \"{dream}\". Дай краткий, этичный разбор: эмоции, символы, динамика, возможный контекст, мягкий вывод. Не более 200 слов."
            }],
            temperature=0.7,
            max_tokens=400
        )
        analysis = response.choices[0].message.content.strip()
    except Exception:
        analysis = "Не удалось проанализировать сон (ошибка API). Попробуй позже."

    # Одна картинка (облегчённая версия)
    image_url = "https://via.placeholder.com/1024x1024.png?text=Картинка+не+сгенерирована"
    try:
        image_response = client.images.generate(
            model="grok-2-image-1212",
            prompt=f"Сюрреалистическая иллюстрация сна: {dream}. Тёмные тона, мечтательная атмосфера, акварель или сюрреализм.",
            n=1,
            size="1024x1024"
        )
        image_url = image_response.data[0].url
    except Exception:
        pass

    conclusion = "Это одна из возможных интерпретаций. Сны индивидуальны. Что ты чувствуешь? 💭"

    return {
        "dream": dream,
        "analysis": analysis,
        "conclusion": conclusion,
        "image_url": image_url
    }

@app.get("/")
async def root():
    return {"message": "UMEQAM Dream Analyzer готов! Отправь POST на /analyze-dream с JSON {dream_text: 'твой сон'} "}

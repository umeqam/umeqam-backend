from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI(title="UMEQAM Dream Analyzer")

try:
    client = OpenAI(
        api_key=os.getenv("XAI_API_KEY"),
        base_url="https://api.x.ai/v1"
    )
except Exception as e:
    client = None  # если ключ плохой

class DreamRequest(BaseModel):
    dream_text: str

@app.post("/analyze-dream")
async def analyze_dream(request: DreamRequest):
    if not request.dream_text.strip():
        raise HTTPException(status_code=400, detail="Описание сна не может быть пустым")

    dream = request.dream_text

    if not client:
        return {"error": "API ключ не настроен. Обратитесь к администратору."}

    analyses = []
    prompts = [
        "Эмоции: Опиши основные эмоции в сне.",
        "Символы: Выдели ключевые символы.",
        "Динамика: Опиши развитие событий.",
        "Контекст: Свяжи с реальной жизнью (мягко)."
    ]

    for prompt in prompts:
        try:
            response = client.chat.completions.create(
                model="grok-4-1-fast-reasoning",
                messages=[{"role": "user", "content": f"Сон: {dream}\n\n{prompt} Кратко."}],
                temperature=0.7,
                max_tokens=200
            )
            analyses.append(response.choices[0].message.content.strip())
        except Exception as e:
            analyses.append("Не удалось проанализировать этот аспект.")

    image_url = "https://via.placeholder.com/1024x1024.png?text=Картинка+не+сгенерирована"
    try:
        image_response = client.images.generate(
            model="grok-2-image-1212",
            prompt=f"Сюрреалистическая иллюстрация сна: {dream}. Тёмные тона, мечтательная атмосфера.",
            n=1,
            size="1024x1024"
        )
        image_url = image_response.data[0].url
    except Exception as e:
        pass

    conclusion = "Это одна из интерпретаций. Сны — зеркало твоего внутреннего мира. Что ты чувствуешь? 💭"

    return {
        "dream": dream,
        "emotions": analyses[0],
        "symbols": analyses[1],
        "dynamics": analyses[2],
        "context": analyses[3],
        "conclusion": conclusion,
        "image_url": image_url
    }

@app.get("/")
async def root():
    return {"message": "UMEQAM Dream Analyzer готов! Отправь POST на /analyze-dream с JSON {dream_text: 'твой сон'} "}
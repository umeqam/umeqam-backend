from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

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

    # 1. Анализ четырьмя "психологами"
    psychologists = [
        "Эмоции: Опиши основные эмоции в этом сне и что они могут значить для сновидца.",
        "Символы: Выдели ключевые символы и объекты в сне, объясни их возможное символическое значение.",
        "Динамика: Опиши, как развивается действие во сне, какие изменения происходят.",
        "Контекст: Свяжи сон с возможными событиями из реальной жизни сновидца (гипотетически, мягко)."
    ]

    analyses = []
    for prompt in psychologists:
        response = client.chat.completions.create(
            model="grok-4-1-fast-reasoning",
            messages=[{"role": "user", "content": f"Сон: {dream}\n\n{prompt} Ответь кратко и по делу."}],
            temperature=0.8,
            max_tokens=300
        )
        analyses.append(response.choices[0].message.content.strip())

    # 2. Генерация картинки
    image_response = client.images.generate(
        model="grok-2-image-1212",
        prompt=f"Сюрреалистическая иллюстрация сна: {dream}. Тёмные тона, мечтательная атмосфера, в стиле Дали и Магритта, высокое качество.",
        n=1,
        size="1024x1024"
    )
    image_url = image_response.data[0].url

    # 3. Мягкий вывод
    conclusion = "Это лишь одна из возможных интерпретаций. Сны — отражение твоего внутреннего мира. Что ты сам чувствуешь по поводу этого сна?"

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
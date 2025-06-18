from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI, File, UploadFile, HTTPException, Header, Depends
from pydantic import BaseModel
from typing import List
from stt_model import transcribe
import os
from groq import Groq

app = FastAPI(
    title="Darwix AI API",
    description="API for transcription and AI title suggestions using Groq",
    version="1.0.0"
)

# API Key Auth
API_KEY = os.getenv("API_KEY", "MY_SUPER_SECRET")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    raise RuntimeError("GROQ_API_KEY not found in environment!")

groq_client = Groq(api_key=GROQ_API_KEY)

async def verify_api_key(x_api_key: str | None = Header(None)):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API key")
    return x_api_key

# Root endpoint
@app.get("/")
def read_root():
    return {"message": "Welcome to Darwix AI FastAPI service."}

# Transcription endpoint
@app.post("/transcribe")
async def transcribe_endpoint(
    file: UploadFile = File(...),
    api_key: str = Depends(verify_api_key)
):
    if file.content_type not in ("audio/wav", "audio/mpeg", "audio/x-wav"):
        raise HTTPException(status_code=400, detail="Please upload a WAV or MP3 file")

    try:
        audio_bytes = await file.read()
        text = transcribe(audio_bytes)
        return {"transcript": text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Transcription failed: {str(e)}")

# Title suggestion endpoint
class TitleRequest(BaseModel):
    text: str

class TitleResponse(BaseModel):
    suggestions: List[str]

@app.post("/api/suggest-titles", response_model=TitleResponse)
async def suggest_titles(data: TitleRequest, api_key: str = Depends(verify_api_key)):
    input_text = data.text.strip()
    if not input_text:
        raise HTTPException(status_code=400, detail="Input text cannot be empty.")

    try:
        prompt = f"Suggest 3 catchy blog titles for this content:\n\n{input_text}\n\nTitles:"
        response = groq_client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[{"role": "user", "content": prompt}]
        )

        content = response.choices[0].message.content.strip()
        suggestions = [
            title.strip("-•123. ").strip()
            for title in content.split("\n")
            if title.strip()
        ][:3]  # Limit to 3

        return {"suggestions": suggestions}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Title generation failed: {str(e)}")

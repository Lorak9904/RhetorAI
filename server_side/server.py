from fastapi import FastAPI, HTTPException, File, UploadFile
import shutil
from pydantic import BaseModel
from mistralai.client import MistralClient
import os
import json
from dotenv import load_dotenv
from typing import List
from whisperrr import transcribe_audio

load_dotenv()

app = FastAPI()

MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")
if not MISTRAL_API_KEY:
    raise ValueError("Missing MISTRAL_API_KEY in .env")

mistral = MistralClient(api_key=MISTRAL_API_KEY)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

class ChatResponse(BaseModel):
    analysis: str
    score: float
    tips: List[str]

@app.get("/")
def home():
    return {"message": "Mistral API is running with Python"}

@app.post("/audio")
async def receive_audio(file: UploadFile = File(...)):
    """Receives a WebM file, transcribes it, and sends the transcription to /chat."""
    
    if not file.filename.endswith(".webm"):
        raise HTTPException(status_code=400, detail="Only WEBM files are allowed")

    file_path = os.path.join(UPLOAD_FOLDER, file.filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    try:
        transcribed_text = transcribe_audio(file_path)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error transcribing audio: {str(e)}")

    chat_response = await chat(transcribed_text)

    return {
        "filename": file.filename,
        "analysis": chat_response.analysis,
        "score": chat_response.score,
        "tips": chat_response.tips
    }

@app.post("/chat", response_model=ChatResponse)
async def chat(audio_text: str):
    """Analyzes transcribed text using Mistral AI."""
    
    enhanced_prompt = (
        f"Please analyze the following text, provide a score between 1 and 100 based on its quality, "
        f"and give some improvement tips. Return the response as a JSON object with the fields "
        f"'analysis', 'score', and 'tips'. Example format:\n"
        f'{{\n'
        f'  "analysis": "...",\n'
        f'  "score": 85,\n'
        f'  "tips": ["...", "..."]\n'
        f'}}\n\n'
        f"Text: {audio_text}\n\n"
    )

    try:
        response = mistral.chat(model="mistral-tiny", messages=[{"role": "user", "content": enhanced_prompt}])
        content = response.choices[0].message.content.strip()

        content = content.replace("'", '"')

        try:
            parsed_response = json.loads(content)
        except json.JSONDecodeError as e:
            raise HTTPException(status_code=500, detail=f"Error decoding JSON: {str(e)}")

        if all(key in parsed_response for key in ['analysis', 'score', 'tips']):
            return ChatResponse(**parsed_response)
        else:
            raise HTTPException(status_code=500, detail="Response is missing required fields.")
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing chat request: {str(e)}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

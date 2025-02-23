import os
import re
import logging
import json
from typing import List
import shutil
from pydantic import BaseModel
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from mistralai.client import MistralClient
from whisperrr import transcribe_audio

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # yeah...
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# mistral key load & client init
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

# healthcheck endpoint
@app.get("/")
def home():
    return {"message": "Mistral API is running with Python"}

# audio transcription
@app.post("/audio")
async def receive_audio(file: UploadFile = File(...)):
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

# log config
logging.basicConfig(level=logging.INFO)

@app.post("/chat", response_model=ChatResponse)
async def chat(audio_text: str):
    """Analyzes transcribed text using Mistral AI."""
    
    enhanced_prompt = (
    f"Analyze the following text and return a JSON response formatted like this:\n"
    f", provide a score between 1 and 100 based on its quality, "
    f"and give some improvement tips. Return the response as a JSON object with the fields "
    f"'analysis', 'score', and 'tips'.\n"
    f"Ensure the response is valid as the provided below JSON with double quotes and no extra commas.\n\n"
    f"Keep in mind the end of line and just make it the cleanest json as possible. It is processed a web application later\n\n"
    f"Example format:\n\n"
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

        logging.info(f"Raw Mistral Response: {content}")

        content = content.replace("'", '"')

        # regex sanitizer
        content = re.sub(r',\s*}', '}', content)
        content = re.sub(r',\s*]', ']', content)

        try:
            parsed_response = json.loads(content)
        except json.JSONDecodeError as e:
            logging.error(f"JSON Decode Error: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Error decoding JSON: {str(e)}")

        if all(key in parsed_response for key in ['analysis', 'score', 'tips']):
            return ChatResponse(**parsed_response)
        else:
            logging.error("Response is missing required fields.")
            raise HTTPException(status_code=500, detail="Response is missing required fields.")
    
    except Exception as e:
        logging.error(f"Error processing chat request: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error processing chat request: {str(e)}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

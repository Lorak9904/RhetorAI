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
    """Analyzes transcribed text using Mistral AI and ensures a valid JSON response."""

    enhanced_prompt = (
        "Analyze the following text and return a JSON response with:\n"
        "- 'analysis': A summary of the quality of the text.\n"
        "- 'score': A number between 1 and 100 evaluating the text quality.\n"
        "- 'tips': A list of improvement suggestions.\n\n"
        "Ensure the JSON is properly formatted, using double quotes for keys and values, "
        "with no extra commas or unnecessary text.\n"
        "Wrap the response in a proper JSON block inside triple backticks like this:\n\n"
        "```\n"
        "{\n"
        '  "analysis": "...",\n'
        '  "score": 85,\n'
        '  "tips": ["...", "..."]\n'
        "}\n"
        "```\n\n"
        "**DO NOT** add explanations, comments, or formatting outside this JSON block."
        "\n\nText:\n" + audio_text
    )

    try:
        # Get the Mistral response
        response = mistral.chat(model="mistral-tiny", messages=[{"role": "user", "content": enhanced_prompt}])
        raw_content = response.choices[0].message.content.strip()

        logging.info(f"Raw Mistral Response: {raw_content}")

        # Check if response is empty or malformed
        if not raw_content:
            logging.error("Mistral response is empty.")
            raise HTTPException(status_code=500, detail="Mistral response is empty.")

        # Extract JSON block using regex
        json_match = re.search(r"```(?:json)?\n([\s\S]+?)\n```", raw_content)
        if json_match:
            json_content = json_match.group(1).strip()
        else:
            logging.error("Failed to extract JSON from response.")
            raise HTTPException(status_code=500, detail="Mistral response does not contain valid JSON.")

        logging.info(f"Extracted JSON: {json_content}")

        # Clean up potential trailing commas
        json_content = re.sub(r',\s*}', '}', json_content)
        json_content = re.sub(r',\s*]', ']', json_content)

        # Parse the cleaned-up JSON
        try:
            parsed_response = json.loads(json_content)
        except json.JSONDecodeError as e:
            logging.error(f"JSON Decode Error: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Error decoding JSON: {str(e)}")

        # Ensure all required fields are present
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

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from mistralai.client import MistralClient
import os
from dotenv import load_dotenv
from typing import List

load_dotenv()

app = FastAPI()

MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")
if not MISTRAL_API_KEY:
    raise ValueError("Missing MISTRAL_API_KEY in .env")

mistral = MistralClient(api_key=MISTRAL_API_KEY)

class ChatRequest(BaseModel):
    prompt: str

class ChatResponse(BaseModel):
    analysis: str
    score: float
    tips: List[str]

@app.get("/")
def home():
    return {"message": "Mistral on Vercel with Python"}

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    try:
        prompt = request.prompt
        
        enhanced_prompt = (
            f"Please analyze the following text, provide a score between 1 and 100 based on its quality, "
            f"and give some improvement tips. Return the response as a JSON object with the fields "
            f"'analysis', 'score', and 'tips'. Example format:\n"
            f"{{\n"
            f"  'analysis': '...',\n"
            f"  'score': 85,\n"
            f"  'tips': ['...', '...']\n"
            f"}}\n\n"
            f"Text: {prompt}\n\n"
        )
        
        response = mistral.chat(model="mistral-tiny", messages=[{"role": "user", "content": enhanced_prompt}])

        content = response.choices[0].message.content.strip()

        try:
            parsed_response = eval(content)
            if all(key in parsed_response for key in ['analysis', 'score', 'tips']):
                return parsed_response
            else:
                raise HTTPException(status_code=500, detail="Response is missing required fields.")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error parsing the model's response: {str(e)}")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing chat request: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

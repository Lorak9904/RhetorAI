from dotenv import load_dotenv
from openai import OpenAI
import os

load_dotenv()

OPENAI_KEY = os.getenv("OPENAI_KEY")
if not OPENAI_KEY:
    raise ValueError("Missing OPENAI_KEY in .env")

openai_client = OpenAI(api_key=OPENAI_KEY)

audio_file = open("miss_south_carolina.mp3", "rb")
transcription = openai_client.audio.transcriptions.create(
    model="whisper-1", 
    file=audio_file,
    response_format="json"
)

print(transcription)
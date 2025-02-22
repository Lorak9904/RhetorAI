from decouple import config
import requests

API_KEY = config("API_KEY")
VOICE_ID = "EXAVITQu4vr4xnSDxMaL"
TEXT = "Hello, world!"

url = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}"
headers = {
    "xi-api-key": API_KEY,
    "Content-Type": "application/json"
}
data = {
    "text": TEXT,
    "voice_settings": {
        "stability": 0.5,
        "similarity_boost": 0.5
    }
}
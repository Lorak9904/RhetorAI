# import whisper
# import os
# ffmpeg_path = "C:/Users/KarolObrebski/Desktop/Coding/Coding/RhetorAI2/venv/Scripts/ffmpeg.exe"
# os.environ["PATH"] += os.pathsep + os.path.dirname(ffmpeg_path)


# model = whisper.load_model("turbo")
# result = model.transcribe("import_audio/miss_south_carolina.mp3")
# print(result["text"])
from decouple import config

from openai import OpenAI
client = OpenAI(api_key=config('OPENAI_API_KEY'))

audio_file = open("import_audio/miss_south_carolina.mp3", "rb")
transcription = client.audio.transcriptions.create(
    model="whisper-1", 
    file=audio_file,
    response_format="verbose_json"
)

print(transcription)
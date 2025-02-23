import os
from google.cloud import speech

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "import_audio/cloud_key.json"

def transcribe_audio(file_path):
    client = speech.SpeechClient()

    with open(file_path, 'rb') as audio_file:
        content = audio_file.read()

    audio = speech.RecognitionAudio(content=content)

    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.FLAC,
        sample_rate_hertz=48000,
        language_code='en-US',
        audio_channel_count=2
    )

    response = client.recognize(config=config, audio=audio)

    for result in response.results:
        print("{}".format(result.alternatives[0].transcript))

audio_file_path = "import_audio/miss_south_carolina.flac"
transcribe_audio(audio_file_path)

import os
from google.cloud import speech
from google.cloud.speech import enums
from google.cloud.speech import types

def transcribe_audio(file_path):
    client = speech.SpeechClient()

    with open(file_path, 'rb') as audio_file:
        content = audio_file.read()

    audio = types.RecognitionAudio(content=content)

    config = types.RecognitionConfig(
        encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,  # Change this to match the sample rate of your audio file
        language_code='en-US',    # Specify the language of the audio
    )

    response = client.recognize(config=config, audio=audio)

    for result in response.results:
        print("Transcript: {}".format(result.alternatives[0].transcript))

audio_file_path = "path/to/your/audio/file.wav"
transcribe_audio(audio_file_path)

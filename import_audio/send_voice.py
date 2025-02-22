import os
from google.cloud import speech

# Set the environment variable for the Google credentials
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "cloud_key.json"  # Ensure the file name is correct

def transcribe_audio(file_path):
    client = speech.SpeechClient()

    with open(file_path, 'rb') as audio_file:
        content = audio_file.read()

    audio = speech.RecognitionAudio(content=content)

    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.FLAC,  # Use FLAC encoding
        sample_rate_hertz=48000,  # Adjusted sample rate to 48000 Hz
        language_code='en-US',    # Specify the language of the audio
        audio_channel_count=2     # Set to 2 for stereo audio
    )

    response = client.recognize(config=config, audio=audio)

    for result in response.results:
        print("{}".format(result.alternatives[0].transcript))

# Make sure the audio file is in the same directory
audio_file_path = "miss_south_carolina.flac"
transcribe_audio(audio_file_path)

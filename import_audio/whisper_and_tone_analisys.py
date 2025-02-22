import json
import numpy as np
import librosa
import librosa.display
from scipy.signal import find_peaks
from openai import OpenAI
from decouple import config

# Initialize OpenAI API
client = OpenAI(api_key=config("OPENAI_API_KEY"))

# Transcribe Audio
audio_file = open("import_audio/miss_south_carolina.mp3", "rb")
transcription = client.audio.transcriptions.create(
    model="whisper-1",
    file=audio_file,
    response_format="verbose_json"
)

# 🔹 Step 1: Detect Disfluencies
def analyze_speech_disfluencies(transcription):
    """
    Detects stuttering, filler words, and calculates speech rate.
    """
    filler_words = {"uh", "um", "like", "you know", "so", "actually"}
    repeated_words = []
    filler_count = 0
    words = []
    
    if "words" in transcription.to_dict():
        words = [word["word"].lower() for word in transcription["words"]]
    else:
        words = transcription["text"].lower().split()  # Fallback

    for i, word in enumerate(words):
        if word in filler_words:
            filler_count += 1
        if i > 0 and words[i - 1] == word:
            repeated_words.append(word)

    speech_rate = len(words) / transcription["duration"] if transcription["duration"] > 0 else 0  

    return {
        "stuttering": repeated_words,
        "filler_count": filler_count,
        "speech_rate": speech_rate
    }

# 🔹 Step 2: Analyze Tone (Confidence, Stress, Anger)
def analyze_tone(audio_path):
    """
    Extracts pitch and volume to estimate confidence, stress, and anger.
    """
    y, sr = librosa.load(audio_path, sr=16000)  # Load audio

    pitch, _ = librosa.piptrack(y=y, sr=sr)  # Extract pitch
    mean_pitch = np.mean(pitch[pitch > 0])  # Ignore zero values

    energy = np.abs(librosa.feature.rms(y=y)).flatten()  # Extract volume
    mean_energy = np.mean(energy)

    peaks, _ = find_peaks(energy, height=mean_energy * 1.5)  # Detect peaks

    tone_analysis = {
        "mean_pitch": mean_pitch,  # Higher → Excited/Angry, Lower → Calm/Confident
        "mean_energy": mean_energy,  # Higher → Confident/Loud, Lower → Hesitant/Soft
        "stress_peaks": len(peaks),  # More peaks → Nervous/Stressed
    }

    return tone_analysis

# Run Analysis
disfluencies = analyze_speech_disfluencies(transcription)
tone = analyze_tone("import_audio/miss_south_carolina.mp3")

# Print Results
print(json.dumps({"disfluencies": disfluencies, "tone_analysis": tone}, indent=4))

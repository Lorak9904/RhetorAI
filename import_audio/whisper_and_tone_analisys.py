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
audio_file = open("import_audio/sutter.mp3", "rb")
transcription = client.audio.transcriptions.create(
    model="whisper-1",
    file=audio_file,
    response_format="verbose_json",
    timestamp_granularities=["word"]
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
    
    if "words" in transcription.to_dict().keys():
        words = [word["word"].lower() for word in transcription.to_dict().get("words")]
    else:
        words = transcription["text"].lower().split()  # Fallback
        pass

    for i, word in enumerate(words):
        if word in filler_words:
            filler_count += 1
        if i > 1 and word in (words[i - 1], words[i - 2], words[i - 3], words[i - 4], words[i - 5], words[i - 6]):            
            repeated_words.append(word)

    speech_rate = len(words) / transcription.to_dict().get('duration') if transcription.to_dict().get("duration") > 0 else 0  

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
tone = analyze_tone("import_audio/sutter.mp3")

# Print Results
# Convert numpy float32 to Python float
def convert_numpy_types(obj):
    if isinstance(obj, np.float32) or isinstance(obj, np.float64):
        return float(obj)
    elif isinstance(obj, dict):
        return {k: convert_numpy_types(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [convert_numpy_types(i) for i in obj]
    return obj

print(json.dumps(convert_numpy_types({"disfluencies": disfluencies, "tone_analysis": tone}), indent=4))
print(transcription.to_dict().get("text"))


x = """
One second, what did you think about the ride? It was great, and apparently I've never been 
on live television before, but apparently sometimes I don't watch the news, because I'm a sutter and apparently every time, apparently Grandpa just gives me a remote after we watch the Powerball. It's the Powerball. Tell me about the ride, what did you think about the ride? Well, it was great, because apparently you're spinning around and apparently every time you get 
dizzy, that's all you do is get dizzy. Is it fun? Yeah, and I've never ever been on live television, I've never ever been on live television. Are you excited? Yeah, and apparently I already went down the super slide. When I went down the slide I was scared half to death. I just freak out. Okay, okay. Wait, I need his name. Hold on, yep, hold on, I'm just going to ask him, what's his name? Noah. Noah, what's your last name? Dick Ritter. How do you spell his last name? Ritter, R-I-T-T-E-R. Okay, and where are you guys from? Wilkes-Barre. Wilkes-Barre, alright buddy. Good stuff. Have fun. We're from three different towns. Oh, right. That is my dad's town, Tom Jersey. Tom's River, New Jersey."""
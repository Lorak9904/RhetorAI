import subprocess
import audioread

def convert_webm_to_mp3(webm_file_path, mp3_file_path):
    try:
        # Check if the file is a valid audio file
        with audioread.audio_open(webm_file_path) as f:
            print(f"Audio file info: {f.channels} channels, {f.samplerate} sample rate, {f.duration} seconds")

        # Convert the WebM file to MP3 using ffmpeg
        command = [
            "ffmpeg",
            "-i", webm_file_path,
            "-vn",  # no video
            "-ar", "44100",  # sample rate
            "-ac", "2",  # stereo audio
            "-b:a", "192k",  # bitrate
            mp3_file_path
        ]
        subprocess.run(command, check=True)
        print(f"Conversion successful! MP3 saved at: {mp3_file_path}")
    except Exception as e:
        print(f"Error occurred during conversion: {e}")

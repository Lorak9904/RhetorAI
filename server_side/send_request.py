import requests

url = "http://127.0.0.1:8000/audio"  # FastAPI audio upload endpoint

# Open the WebM file in binary mode
with open("dupa.webm", "rb") as file:
    files = {"file": ("dupa.webm", file, "audio/webm")}  # Multipart file upload

    response = requests.post(url, files=files)  # Send request

print(response.text)  # Print the response

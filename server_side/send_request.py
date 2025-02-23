import requests

# testing utility

url = "http://127.0.0.1:8000/audio"

with open("dupa.webm", "rb") as file:
    files = {"file": ("dupa.webm", file, "audio/webm")}

    response = requests.post(url, files=files)

print(response.text)

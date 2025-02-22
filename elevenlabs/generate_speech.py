import requests
from config_api import API_KEY, VOICE_ID, TEXT, url, headers, data

response = requests.post(url, json=data, headers=headers)

if response.status_code == 200:
    with open("output.mp3", "wb") as f:
        f.write(response.content)
    print("Audio saved as output.mp3")
else:
    print(f"Error: {response.status_code}, {response.text}")

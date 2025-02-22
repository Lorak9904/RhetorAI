import requests
import json

url = 'http://127.0.0.1:8000/chat'
headers = {'Content-Type': 'application/json'}
data = {
    "prompt": "I personally believe that U.S. Americans are unable to do so because some people out there in our nation don't have maps and I believe that our education, like such as in South Africa and the Iraq, everywhere like such as and I believe that they should, our education over here in the U.S. should help the U.S. or should help South Africa and should help the Iraq and the Asian countries so we will be able to build up our future for our children. Thank you very much, South Carolina."
}

response = requests.post(url, headers=headers, data=json.dumps(data))

# Print the response from the server
print(response.text)

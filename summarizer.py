import requests
from dotenv import load_dotenv
import os

load_dotenv()

pplx_api_key = os.getenv("PPLX_API_KEY")
model = os.getenv("MODEL")

with open("link", "r") as f:
    article_link = f.read().strip()


headers = {
    'accept': 'application/json',
    'authorization': 'Bearer ' + pplx_api_key,
    'content-type': 'application/json',
}

json_data = {
    'model': model,
    'messages': [
        {
            'role': 'system',
            'content': 'Be precise, concise and clear',
        },
        {
            'role': 'user',
            'content': 'Search and summarize: ' + article_link,
        },
    ],
}

response = requests.post('https://api.perplexity.ai/chat/completions', headers=headers, json=json_data)

response = response.json()
#print(response)

#print(response["choices"][0]["message"]["content"])
with open("response", "w+") as response_file:
    response_file.write(response["choices"][0]["message"]["content"])
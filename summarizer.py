import requests

def summarize(link, pplx_api_key, model):
    headers = {
        "accept": "application/json",
        "authorization": "Bearer " + pplx_api_key,
        "content-type": "application/json",
    }

    json_data = {
        "model": model,
        "messages": [
            {
                "role": "system",
                "content": "Be precise, concise and clear. Also proofread what you write and make sure not to hallucinate.",
            },
            {
                "role": "user",
                "content": "Read and summarize: " + link,
            },
        ],
    }

    response = requests.post(
        "https://api.perplexity.ai/chat/completions",
        headers=headers,
        json=json_data,
        timeout=5,
    )

    response = response.json()
    # print(response)
    try:
        return response["choices"][0]["message"]["content"]
    except Exception as e:
        return "Error: " + str(e)
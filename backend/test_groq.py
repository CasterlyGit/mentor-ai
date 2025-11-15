import requests

# Paste your actual key here directly
api_key = "gsk_eXByXIzfwQum2g9LLZ0sWGdyb3FYCNCtBRp6KR5PJWA3LLIrSPFve"

print(f"API Key: {api_key[:10]}...")

response = requests.post(
    "https://api.groq.com/openai/v1/chat/completions",
    headers={"Authorization": f"Bearer {api_key}"},
    json={
        "model": "llama3-8b-8192",
        "messages": [{"role": "user", "content": "Say hello world"}],
        "temperature": 0.3
    }
)

print(f"Status Code: {response.status_code}")

if response.status_code == 200:
    print("SUCCESS! API is working")
    print("Message:", response.json()["choices"][0]["message"]["content"])
else:
    print("ERROR: API call failed")
    print("Response:", response.text)

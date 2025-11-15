from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import screen_capture
import voice_capture
import requests
import os
import uvicorn

# Load environment variables from .env file - EXPLICIT PATH
env_path = os.path.join(os.path.dirname(__file__), '.env')
print(f"Loading .env from: {env_path}")
load_dotenv(env_path)

# Debug: Check if API key is loaded
api_key = os.getenv("GROQ_API_KEY")
if api_key:
    print(f"✅ API Key loaded: {api_key[:10]}...")
else:
    print("❌ API Key NOT loaded!")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_ai_response(question):
    api_key = os.getenv("GROQ_API_KEY")
    
    if not api_key or api_key == "gsk_yourActualKeyHere":
        return "ERROR: GROQ_API_KEY not properly configured in .env file"
    
    try:
        response = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers={"Authorization": f"Bearer {api_key}"},
            json={
                "model": "llama-3.1-8b-instant",
                "messages": [{"role": "user", "content": f"User asks: {question}. Give short coding help."}],
                "temperature": 0.3
            },
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            if 'choices' in data and len(data['choices']) > 0:
                return data['choices'][0]['message']['content']
            else:
                return "AI response format error: No choices found"
        else:
            return f"API Error {response.status_code}: {response.text}"
            
    except Exception as e:
        return f"AI error: {str(e)}"

@app.post("/ask")
async def ask_mentor():
    screenshot = screen_capture.capture_screen()
    question = voice_capture.record_and_transcribe()
    answer = get_ai_response(question)
    
    return {
        "question": question,
        "answer": answer,
        "screenshot_length": len(screenshot)
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

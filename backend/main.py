from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import screen_capture
import voice_capture
import requests
import os
import uvicorn

# Load environment variables from .env file
load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_ai_response(question):
    api_key = os.getenv("GROQ_API_KEY")
    
    if not api_key:
        return "ERROR: GROQ_API_KEY not found in environment variables"
    
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

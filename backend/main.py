from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import screen_capture
import voice_capture
import requests
import os
import uvicorn

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_ai_response(question):
    api_key = os.getenv("GROQ_API_KEY")
    
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
        return response.json()["choices"][0]["message"]["content"]
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

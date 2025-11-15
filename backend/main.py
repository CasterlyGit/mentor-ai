from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import screen_capture
import voice_capture
import requests
import os
import uvicorn
from memory_manager import MemoryManager
from performance_monitor import monitor

# FORCE RELOAD - Clear any cached environment variables
if 'GROQ_API_KEY' in os.environ:
    del os.environ['GROQ_API_KEY']

# Load environment variables FRESH
env_path = os.path.join(os.path.dirname(__file__), '.env')
print(f"🔄 Loading from: {env_path}")
load_dotenv(env_path, override=True)  # Force override

# Get API key
api_key = os.getenv("GROQ_API_KEY")
print(f"✅ API Key in main: {api_key}")

if not api_key or api_key.startswith('gsk_your'):
    print("❌ WRONG KEY LOADED!")
else:
    print("✅ CORRECT KEY LOADED!")

# Initialize systems
memory = MemoryManager()

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

def get_ai_response(question):
    global api_key
    
    if not api_key or api_key.startswith('gsk_your'):
        return f"ERROR: Wrong API key loaded: {api_key[:20] if api_key else 'None'}"
    
    try:
        response = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers={"Authorization": f"Bearer {api_key}"},
            json={
                "model": "llama-3.1-8b-instant",
                "messages": [{"role": "user", "content": f"User: {question}. Give coding help."}],
                "temperature": 0.3
            },
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            return data['choices'][0]['message']['content']
        else:
            return f"API Error: {response.text}"
            
    except Exception as e:
        return f"Error: {str(e)}"

@app.post("/ask")
async def ask_mentor():
    start_time = monitor.start_request()
    screenshot = screen_capture.capture_screen()
    question = voice_capture.record_and_transcribe()
    context = memory.get_context()
    
    enhanced_question = f"Context:\n{context}\n\nCurrent: {question}"
    answer = get_ai_response(enhanced_question)
    
    memory.add_exchange(question, answer, screenshot)
    stats = memory.get_stats()
    perf_stats = monitor.end_request(start_time)
    
    return {
        "question": question,
        "answer": answer,
        "screenshot_length": len(screenshot),
        "session_stats": stats,
        "performance_stats": perf_stats
    }

@app.get("/stats")
async def get_stats():
    return {
        "performance": monitor.get_performance_stats(),
        "memory": memory.get_stats()
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

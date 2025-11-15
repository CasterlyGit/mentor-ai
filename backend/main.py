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
from code_analyzer import CodeAnalyzer

# Load environment
env_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(env_path, override=True)

api_key = os.getenv("GROQ_API_KEY")
print(f"✅ API Key: {api_key[:10]}...")

# Initialize systems
memory = MemoryManager()
code_analyzer = CodeAnalyzer()

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

def get_ai_response(question, code_context=None):
    global api_key
    
    if not api_key:
        return "ERROR: No API key"
    
    # Build prompt
    prompt = f"User asks: {question}. Provide coding help."
    
    if code_context and code_context.get('language') != 'unknown' and code_context.get('code_snippets'):
        prompt += f"\n\nDetected {code_context['language']} code:\n" + "\n".join([f"```{snippet}```" for snippet in code_context['code_snippets']])
    
    try:
        response = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers={"Authorization": f"Bearer {api_key}"},
            json={
                "model": "llama-3.1-8b-instant",
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0.3
            },
            timeout=10
        )
        
        if response.status_code == 200:
            return response.json()['choices'][0]['message']['content']
        else:
            return f"API Error: {response.status_code}"
            
    except Exception as e:
        return f"Error: {str(e)}"

@app.post("/ask")
async def ask_mentor():
    start_time = monitor.start_request()
    
    screenshot = screen_capture.capture_screen()
    question = voice_capture.record_and_transcribe()
    
    # Try code analysis
    code_analysis = code_analyzer.extract_code_from_image(screenshot)
    print(f"🔍 Code Analysis: {code_analysis['language']} (conf: {code_analysis['confidence']})")
    
    # Get AI response
    context = memory.get_context()
    enhanced_question = f"Context:\\n{context}\\n\\nQuestion: {question}"
    answer = get_ai_response(enhanced_question, code_analysis)
    
    # Store results
    memory.add_exchange(question, answer, screenshot)
    stats = memory.get_stats()
    perf_stats = monitor.end_request(start_time)
    
    return {
        "question": question,
        "answer": answer,
        "screenshot_length": len(screenshot),
        "code_analysis": code_analysis,
        "session_stats": stats,
        "performance_stats": perf_stats
    }

@app.get("/stats")
async def get_stats():
    return {"performance": monitor.get_performance_stats(), "memory": memory.get_stats()}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "systems": ["memory", "code_analyzer", "performance_monitor"]}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

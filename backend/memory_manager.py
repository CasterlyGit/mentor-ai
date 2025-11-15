import json
import os
from datetime import datetime

class MemoryManager:
    def __init__(self):
        self.session_file = "session_memory.json"
        self.conversation_history = []
        self.load_memory()
    
    def load_memory(self):
        if os.path.exists(self.session_file):
            with open(self.session_file, 'r') as f:
                self.conversation_history = json.load(f)
    
    def save_memory(self):
        with open(self.session_file, 'w') as f:
            json.dump(self.conversation_history[-10:], f)  # Keep last 10 exchanges
    
    def add_exchange(self, question, answer, screenshot_data=None):
        exchange = {
            "timestamp": datetime.now().isoformat(),
            "question": question,
            "answer": answer,
            "screenshot_length": len(screenshot_data) if screenshot_data else 0
        }
        self.conversation_history.append(exchange)
        self.save_memory()
    
    def get_context(self, max_exchanges=3):
        """Get recent context for AI prompts"""
        recent = self.conversation_history[-max_exchanges:]
        context = []
        for exchange in recent:
            context.append(f"Previous Q: {exchange['question']}")
            context.append(f"Previous A: {exchange['answer'][:100]}...")
        return "\n".join(context) if context else "No previous context"
    
    def get_stats(self):
        return {
            "total_exchanges": len(self.conversation_history),
            "session_start": self.conversation_history[0]['timestamp'] if self.conversation_history else "No session",
            "recent_activity": len([e for e in self.conversation_history 
                                  if datetime.fromisoformat(e['timestamp']).date() == datetime.now().date()])
        }

# Test the memory system
if __name__ == "__main__":
    memory = MemoryManager()
    print("Memory Manager Test:", memory.get_stats())

import tkinter as tk
import threading
import requests

class MentorApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Mentor AI - Your Coding Assistant")
        self.root.geometry("600x500")
        
        # Header
        header = tk.Label(self.root, text="🤖 Mentor AI", 
                         font=('Arial', 20, 'bold'), fg='#2E86AB')
        header.pack(pady=20)
        
        # Instructions
        instructions = tk.Label(self.root, 
                               text="Click the button below, then speak your coding question for 5 seconds.\nI'll analyze your screen and help you!",
                               font=('Arial', 12), wraplength=500)
        instructions.pack(pady=10)
        
        # Question display
        self.question_label = tk.Label(self.root, text="Your question will appear here...", 
                                      wraplength=550, font=('Arial', 11), fg='#A23B72')
        self.question_label.pack(pady=15)
        
        # Answer display
        self.answer_label = tk.Label(self.root, text="AI response will appear here...", 
                                    wraplength=550, justify='left', font=('Arial', 10))
        self.answer_label.pack(pady=15, fill='both', expand=True)
        
        # Action button
        self.ask_button = tk.Button(self.root, text="🎤 Ask Mentor AI", 
                                   command=self.ask_mentor, 
                                   font=('Arial', 14), bg='#4CAF50', fg='white',
                                   height=2, width=20)
        self.ask_button.pack(pady=20)
        
        # Status
        status = tk.Label(self.root, text="Phase 1 MVP: Screen + Voice + AI Integration ✅", 
                         font=('Arial', 9), fg='gray')
        status.pack(pady=10)
    
    def ask_mentor(self):
        """Trigger the mentor AI via your existing backend API"""
        def make_request():
            try:
                self.ask_button.config(state='disabled', text="🔄 Processing...")
                self.question_label.config(text="🎤 Recording... Speak now!")
                self.answer_label.config(text="📸 Capturing screen...\n🎙️ Listening for 5 seconds...\n🤔 Analyzing with AI...")
                self.root.update()
                
                # Call your existing backend API
                response = requests.post('http://localhost:8000/ask', timeout=30)
                data = response.json()
                
                # Update UI with results
                self.question_label.config(text=f"❓ {data['question']}")
                self.answer_label.config(text=f"💡 {data['answer']}")
                
            except Exception as e:
                self.answer_label.config(text=f"❌ Error: {str(e)}\n\nMake sure the backend is running!\nRun: python main.py")
            finally:
                self.ask_button.config(state='normal', text="🎤 Ask Mentor AI")
        
        # Run in thread to avoid freezing UI
        thread = threading.Thread(target=make_request)
        thread.start()
    
    def run(self):
        print("🚀 Mentor AI Desktop App Started!")
        print("💡 Make sure to start the backend first:")
        print("   cd backend && python main.py")
        print("📝 Then click 'Ask Mentor AI' and speak your question!")
        self.root.mainloop()

if __name__ == "__main__":
    app = MentorApp()
    app.run()

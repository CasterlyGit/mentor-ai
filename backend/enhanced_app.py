import tkinter as tk
from tkinter import ttk, scrolledtext
import threading
import requests
import json
from hotkey_manager import HotkeyManager

class EnhancedMentorApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Mentor AI Pro")
        self.root.geometry("700x600")
        self.root.configure(bg='#1e1e1e')
        
        self.setup_ui()
        self.setup_hotkeys()
        
    def setup_ui(self):
        # Header
        header_frame = tk.Frame(self.root, bg='#1e1e1e')
        header_frame.pack(fill='x', padx=20, pady=10)
        
        title = tk.Label(header_frame, text="🤖 Mentor AI Pro", 
                        font=('Arial', 24, 'bold'), fg='#2E86AB', bg='#1e1e1e')
        title.pack()
        
        subtitle = tk.Label(header_frame, text="Your AI Coding Assistant", 
                           font=('Arial', 12), fg='#A23B72', bg='#1e1e1e')
        subtitle.pack()
        
        # Stats frame
        stats_frame = tk.Frame(self.root, bg='#2e2e2e', relief='raised', bd=1)
        stats_frame.pack(fill='x', padx=20, pady=5)
        
        stats_text = "🚀 Phase 2 Active | 🎯 Cmd+Shift+M | 🎤 Voice + 📸 Screen"
        stats_label = tk.Label(stats_frame, text=stats_text, 
                              font=('Arial', 10), fg='white', bg='#2e2e2e')
        stats_label.pack(pady=5)
        
        # Main content
        content_frame = tk.Frame(self.root, bg='#1e1e1e')
        content_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Question display
        q_label = tk.Label(content_frame, text="QUESTION:", 
                          font=('Arial', 11, 'bold'), fg='#88c0d0', bg='#1e1e1e')
        q_label.pack(anchor='w')
        
        self.question_text = scrolledtext.ScrolledText(content_frame, 
                                                     height=3, width=80,
                                                     font=('Arial', 10),
                                                     bg='#2e2e2e', fg='white',
                                                     insertbackground='white')
        self.question_text.pack(fill='x', pady=(5, 15))
        
        # Answer display
        a_label = tk.Label(content_frame, text="AI RESPONSE:", 
                          font=('Arial', 11, 'bold'), fg='#a3be8c', bg='#1e1e1e')
        a_label.pack(anchor='w')
        
        self.answer_text = scrolledtext.ScrolledText(content_frame, 
                                                   height=15, width=80,
                                                   font=('Arial', 10),
                                                   bg='#2e2e2e', fg='white',
                                                   insertbackground='white')
        self.answer_text.pack(fill='both', expand=True, pady=(5, 15))
        
        # Controls
        controls_frame = tk.Frame(content_frame, bg='#1e1e1e')
        controls_frame.pack(fill='x', pady=10)
        
        self.ask_btn = tk.Button(controls_frame, text="🎤 ASK MENTOR AI", 
                                command=self.ask_mentor,
                                font=('Arial', 12, 'bold'), 
                                bg='#4CAF50', fg='white',
                                height=2, width=20)
        self.ask_btn.pack(side='left', padx=(0, 10))
        
        clear_btn = tk.Button(controls_frame, text="🗑️ CLEAR", 
                             command=self.clear_chat,
                             font=('Arial', 10), 
                             bg='#f44336', fg='white')
        clear_btn.pack(side='left', padx=(0, 10))
        
        quit_btn = tk.Button(controls_frame, text="🔚 QUIT", 
                            command=self.root.quit,
                            font=('Arial', 10), 
                            bg='#ff9800', fg='white')
        quit_btn.pack(side='left')
        
        # Status bar
        self.status_var = tk.StringVar()
        self.status_var.set("Ready - Press Cmd+Shift+M or click Ask Mentor")
        status_bar = tk.Label(self.root, textvariable=self.status_var,
                             font=('Arial', 9), fg='gray', bg='#1e1e1e',
                             relief='sunken', bd=1)
        status_bar.pack(fill='x', side='bottom')
    
    def setup_hotkeys(self):
        self.hotkey_manager = HotkeyManager(self.ask_mentor)
        self.hotkey_manager.start()
    
    def ask_mentor(self):
        def make_request():
            try:
                self.status_var.set("🔄 Processing request...")
                self.ask_btn.config(state='disabled', text="🔄 PROCESSING...")
                
                response = requests.post('http://localhost:8000/ask', timeout=30)
                data = response.json()
                
                # Update UI
                self.question_text.delete(1.0, tk.END)
                self.question_text.insert(1.0, data['question'])
                
                self.answer_text.delete(1.0, tk.END)
                self.answer_text.insert(1.0, data['answer'])
                
                self.status_var.set(f"✅ Done - Screenshot: {data['screenshot_length']} bytes")
                
            except Exception as e:
                self.status_var.set(f"❌ Error: {str(e)}")
                self.answer_text.delete(1.0, tk.END)
                self.answer_text.insert(1.0, f"Error: {str(e)}\n\nMake sure backend is running: python main.py")
            finally:
                self.ask_btn.config(state='normal', text="🎤 ASK MENTOR AI")
        
        thread = threading.Thread(target=make_request)
        thread.start()
    
    def clear_chat(self):
        self.question_text.delete(1.0, tk.END)
        self.answer_text.delete(1.0, tk.END)
        self.status_var.set("Chat cleared")
    
    def run(self):
        print("🚀 Mentor AI Pro Started!")
        print("🎯 Features: Global Hotkeys (Cmd+Shift+M) + Enhanced UI")
        self.root.mainloop()

if __name__ == "__main__":
    app = EnhancedMentorApp()
    app.run()

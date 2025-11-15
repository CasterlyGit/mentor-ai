import tkinter as tk
from tkinter import scrolledtext
import threading
import requests
from code_analyzer import CodeAnalyzer
from screen_capture import capture_screen
from voice_capture import record_and_transcribe

class PersistentOverlay:
    def __init__(self):
        self.root = tk.Tk()
        self.root.overrideredirect(True)
        self.root.attributes('-topmost', True)
        self.root.attributes('-alpha', 0.95)
        self.root.configure(bg='#0f0f23')
        
        # Position at top-right corner
        screen_width = self.root.winfo_screenwidth()
        self.root.geometry(f"500x600+{screen_width-520}+50")
        
        self.code_analyzer = CodeAnalyzer()
        self.setup_ui()
        
    def setup_ui(self):
        # Header
        header = tk.Frame(self.root, bg='#1a1a2e', height=50)
        header.pack(fill='x')
        header.pack_propagate(False)
        
        title = tk.Label(header, text="🧠 Code Mentor", bg='#1a1a2e', fg='#64ffda', 
                        font=('Arial', 14, 'bold'))
        title.place(x=10, y=12)
        
        # Close button
        close_btn = tk.Button(header, text="✕", command=self.root.quit,
                             bg='#ff5f56', fg='white', font=('Arial', 12), 
                             border=0, width=3)
        close_btn.place(x=470, y=8)
        
        # Main content area
        content = tk.Frame(self.root, bg='#0f0f23')
        content.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Ask button
        self.ask_btn = tk.Button(content, text="🎤 Ask About This Code", 
                                command=self.ask_about_code,
                                bg='#00d4aa', fg='white', font=('Arial', 12, 'bold'),
                                border=0, padx=20, pady=10, width=25)
        self.ask_btn.pack(pady=(0, 15))
        
        # Code analysis display
        analysis_frame = tk.Frame(content, bg='#1a1a2e', relief='raised', bd=1)
        analysis_frame.pack(fill='x', pady=(0, 10))
        
        analysis_label = tk.Label(analysis_frame, text="📊 Code Analysis", 
                                 bg='#1a1a2e', fg='#64ffda', font=('Arial', 11, 'bold'))
        analysis_label.pack(anchor='w', padx=10, pady=5)
        
        self.analysis_text = tk.Label(analysis_frame, text="No code detected yet", 
                                     bg='#1a1a2e', fg='#8892b0', font=('Arial', 9),
                                     justify='left', wraplength=460)
        self.analysis_text.pack(fill='x', padx=10, pady=(0, 10))
        
        # Response area
        response_label = tk.Label(content, text="💡 AI Response", 
                                 bg='#0f0f23', fg='#64ffda', font=('Arial', 11, 'bold'),
                                 justify='left')
        response_label.pack(anchor='w', pady=(10, 5))
        
        self.response_area = scrolledtext.ScrolledText(content, 
                                                     wrap=tk.WORD,
                                                     width=55, 
                                                     height=20,
                                                     bg='#1a1a2e', 
                                                     fg='#e6f1ff',
                                                     font=('Arial', 9),
                                                     border=1,
                                                     relief='flat',
                                                     insertbackground='white')
        self.response_area.pack(fill='both', expand=True)
        self.response_area.insert(tk.END, "Click 'Ask About This Code' and speak your question...")
        self.response_area.config(state='disabled')
        
        # Auto-refresh code analysis every 10 seconds
        self.auto_refresh()
    
    def auto_refresh(self):
        """Automatically refresh code analysis"""
        self.analyze_current_screen()
        self.root.after(10000, self.auto_refresh)  # Refresh every 10 seconds
    
    def analyze_current_screen(self):
        """Analyze code from current screen"""
        try:
            screenshot = capture_screen()
            analysis = self.code_analyzer.extract_code_from_image(screenshot)
            
            if analysis['language'] != 'unknown' and analysis['confidence'] > 0.2:
                analysis_text = f"🔍 {analysis['language'].upper()} code detected (confidence: {analysis['confidence']})\n"
                if analysis['code_snippets']:
                    analysis_text += f"📝 Snippets: {len(analysis['code_snippets'])} lines"
                self.analysis_text.config(text=analysis_text, fg='#4cc9f0')
            else:
                self.analysis_text.config(text="❌ No code detected - open a code file", fg='#ff6b6b')
                
        except Exception as e:
            self.analysis_text.config(text=f"⚠️ Analysis error: {str(e)}", fg='#ffa500')
    
    def ask_about_code(self):
        """Ask AI about the current code on screen"""
        def process_request():
            try:
                self.ask_btn.config(state='disabled', text="🔄 Analyzing...")
                self.response_area.config(state='normal')
                self.response_area.delete(1.0, tk.END)
                self.response_area.insert(tk.END, "🎤 Listening... speak your question now!\n")
                self.root.update()
                
                # Capture current screen and voice
                screenshot = capture_screen()
                question = record_and_transcribe()
                
                self.response_area.insert(tk.END, f"📝 You asked: {question}\n\n")
                self.response_area.insert(tk.END, "🤔 Analyzing code and thinking...\n")
                self.root.update()
                
                # Analyze code
                code_analysis = self.code_analyzer.extract_code_from_image(screenshot)
                
                # Call backend API
                response = requests.post('http://localhost:8000/ask', timeout=30)
                data = response.json()
                
                # Display results
                self.response_area.insert(tk.END, f"💡 AI Response:\n{data['answer']}\n\n")
                
                # Show code analysis summary
                if code_analysis['language'] != 'unknown':
                    self.response_area.insert(tk.END, f"📊 Code Analysis: {code_analysis['language']} (confidence: {code_analysis['confidence']})\n")
                
                self.response_area.see(tk.END)
                self.response_area.config(state='disabled')
                
            except Exception as e:
                self.response_area.config(state='normal')
                self.response_area.insert(tk.END, f"❌ Error: {str(e)}\n\nMake sure backend is running: python main.py")
                self.response_area.config(state='disabled')
                self.response_area.see(tk.END)
            finally:
                self.ask_btn.config(state='normal', text="🎤 Ask About This Code")
                # Refresh analysis display
                self.analyze_current_screen()
        
        thread = threading.Thread(target=process_request)
        thread.start()
    
    def run(self):
        print("🚀 Persistent Code Mentor Overlay Started!")
        print("📍 Always on top - Drag to reposition")
        print("🔄 Auto-refreshes code analysis every 10 seconds")
        print("🎤 Click 'Ask About This Code' to get help")
        self.root.mainloop()

if __name__ == "__main__":
    overlay = PersistentOverlay()
    overlay.run()

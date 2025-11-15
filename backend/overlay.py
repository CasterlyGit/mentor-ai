import tkinter as tk
from tkinter import scrolledtext
from screen_capture import capture_screen
from voice_capture import record_and_transcribe
from main import get_ai_response

class SimpleOverlay:
    def __init__(self):
        self.root = tk.Tk()
        self.root.overrideredirect(True)
        self.root.attributes('-topmost', True)
        self.root.attributes('-alpha', 0.95)
        self.root.configure(bg='#1a1a1a')
        
        # Position at top-right
        screen_width = self.root.winfo_screenwidth()
        self.root.geometry(f"500x400+{screen_width-520}+50")
        
        # Header
        header = tk.Frame(self.root, bg='#2d2d2d', height=40)
        header.pack(fill='x')
        header.pack_propagate(False)
        
        title = tk.Label(header, text="🤖 Mentor AI", bg='#2d2d2d', fg='white', 
                        font=('Arial', 14, 'bold'))
        title.place(x=10, y=8)
        
        close_btn = tk.Button(header, text="✕", command=self.root.quit,
                             bg='#ff5f56', fg='white', font=('Arial', 12), 
                             border=0, width=3)
        close_btn.place(x=460, y=8)
        
        # Ask button
        ask_btn = tk.Button(self.root, text="🎤 Ask Mentor", command=self.ask,
                           bg='#10b981', fg='white', font=('Arial', 12, 'bold'),
                           border=0, padx=20, pady=8)
        ask_btn.pack(pady=10)
        
        # Scrollable text area
        self.text_area = scrolledtext.ScrolledText(self.root, 
                                                  wrap=tk.WORD,
                                                  width=55, 
                                                  height=18,
                                                  bg='#1a1a1a', 
                                                  fg='white',
                                                  font=('Arial', 10),
                                                  border=1,
                                                  relief='flat')
        self.text_area.pack(padx=10, pady=5, fill='both', expand=True)
        self.text_area.insert(tk.END, "Click 'Ask Mentor' and speak for 5 seconds...")
        self.text_area.config(state='disabled')
    
    def ask(self):
        self.text_area.config(state='normal')
        self.text_area.delete(1.0, tk.END)
        self.text_area.insert(tk.END, "🎤 Recording... Speak now!\n")
        self.root.update()
        
        question = record_and_transcribe()
        self.text_area.insert(tk.END, f"\n❓ Q: {question}\n")
        self.text_area.insert(tk.END, "🤔 Thinking...\n")
        self.root.update()
        
        answer = get_ai_response(question)
        self.text_area.insert(tk.END, f"\n💡 A: {answer}\n")
        self.text_area.config(state='disabled')
        self.text_area.see(tk.END)
    
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    overlay = SimpleOverlay()
    overlay.run()

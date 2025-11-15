import tkinter as tk
from tkinter import messagebox
import threading
import pystray
from PIL import Image, ImageDraw
import screen_capture
import voice_capture
from main import get_ai_response
from hotkey_manager import HotkeyManager

class SystemTrayApp:
    def __init__(self):
        self.create_tray_icon()
        self.hotkey_manager = None
        
    def create_tray_icon(self):
        # Create a simple icon
        image = Image.new('RGB', (64, 64), color='#2E86AB')
        draw = ImageDraw.Draw(image)
        draw.ellipse((16, 16, 48, 48), fill='#A23B72')
        
        # Create tray icon menu
        menu = pystray.Menu(
            pystray.MenuItem('Ask Mentor', self.ask_mentor),
            pystray.MenuItem('Settings', self.show_settings),
            pystray.MenuItem('Exit', self.exit_app)
        )
        
        self.icon = pystray.Icon("mentor_ai", image, "Mentor AI", menu)
        
    def ask_mentor(self):
        def process_request():
            try:
                question = voice_capture.record_and_transcribe()
                answer = get_ai_response(question)
                self.show_notification("Mentor AI", answer[:100] + "...")
            except Exception as e:
                self.show_notification("Error", str(e))
                
        thread = threading.Thread(target=process_request)
        thread.start()
        
    def show_settings(self, icon, item):
        messagebox.showinfo("Settings", "Mentor AI is running in background.\n\nHotkey: Cmd+Shift+M\n\nStatus: Active")
        
    def show_notification(self, title, message):
        try:
            # macOS notification
            import subprocess
            subprocess.run(['osascript', '-e', f'display notification "{message}" with title "{title}"'])
        except:
            pass
            
    def start_hotkeys(self):
        self.hotkey_manager = HotkeyManager(self.ask_mentor)
        self.hotkey_manager.start()
        
    def exit_app(self, icon, item):
        if self.hotkey_manager:
            self.hotkey_manager.stop()
        self.icon.stop()
        
    def run(self):
        self.start_hotkeys()
        print("🚀 Mentor AI running in system tray!")
        print("📌 Cmd+Shift+M to activate anytime")
        print("🖱️  Click tray icon for menu")
        self.icon.run()

if __name__ == "__main__":
    app = SystemTrayApp()
    app.run()

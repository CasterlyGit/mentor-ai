import threading
from pynput import keyboard
import requests
import json

class HotkeyManager:
    def __init__(self, callback):
        self.callback = callback
        self.listener = None
        
    def start(self):
        def on_activate():
            self.callback()
            return False
            
        # Define hotkey combination
        hotkey = keyboard.HotKey(
            keyboard.HotKey.parse('<cmd>+<shift>+m'),
            on_activate
        )
        
        def for_canonical(f):
            return lambda k: f(self.listener.canonical(k))
            
        self.listener = keyboard.Listener(
            on_press=for_canonical(hotkey.press),
            on_release=for_canonical(hotkey.release)
        )
        self.listener.start()
        
    def stop(self):
        if self.listener:
            self.listener.stop()

# Test the hotkey
if __name__ == "__main__":
    def test_callback():
        print("Hotkey activated! Cmd+Shift+M pressed")
        
    manager = HotkeyManager(test_callback)
    manager.start()
    print("Hotkey listener started. Press Cmd+Shift+M to test.")
    
    # Keep the program running
    try:
        while True:
            pass
    except KeyboardInterrupt:
        manager.stop()

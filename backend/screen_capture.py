import subprocess
import base64
import tempfile
import os

def capture_screen():
    try:
        with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp_file:
            temp_path = tmp_file.name
        
        subprocess.run(['screencapture', '-x', temp_path], check=True)
        
        with open(temp_path, 'rb') as f:
            image_data = f.read()
        
        os.unlink(temp_path)
        return base64.b64encode(image_data).decode()
        
    except Exception as e:
        return f"Error: {str(e)}"

if __name__ == "__main__":
    print("Screen capture working:", len(capture_screen()) > 100)

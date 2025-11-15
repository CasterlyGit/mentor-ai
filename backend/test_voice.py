import whisper
import sounddevice as sd
import numpy as np
from scipy.io.wavfile import write
import tempfile

def test_whisper():
    print("Testing Whisper...")
    
    # Test loading model
    model = whisper.load_model("base")
    print("✓ Whisper model loaded successfully")
    
    # Create a simple test audio (1 second of silence)
    print("Creating test audio...")
    sample_rate = 16000
    duration = 1  # seconds
    audio_data = np.zeros(int(duration * sample_rate))
    
    # Save to temporary file
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp_file:
        write(tmp_file.name, sample_rate, (audio_data * 32767).astype(np.int16))
        
        # Test transcription
        result = model.transcribe(tmp_file.name)
        print(f"✓ Transcription test passed: '{result['text']}'")
    
    print("All tests passed! Whisper is working.")

if __name__ == "__main__":
    test_whisper()

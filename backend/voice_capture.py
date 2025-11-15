import whisper
import sounddevice as sd
import numpy as np
from scipy.io.wavfile import write
import tempfile

def record_and_transcribe():
    try:
        # Record audio
        duration = 5
        sample_rate = 16000
        print(f"Recording {duration} seconds...")
        audio = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1)
        sd.wait()
        
        # Save and transcribe
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as f:
            write(f.name, sample_rate, (audio * 32767).astype(np.int16))
            model = whisper.load_model("base")
            result = model.transcribe(f.name)
            
        return result["text"]
    except Exception as e:
        return f"Voice error: {str(e)}"

if __name__ == "__main__":
    text = record_and_transcribe()
    print("Transcribed:", text)

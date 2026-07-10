import os
import tempfile
from faster_whisper import WhisperModel

model_size = "tiny"
# Run on CPU with INT8 for fast local inference
model = WhisperModel(model_size, device="cpu", compute_type="int8")

def transcribe_audio(audio_bytes: bytes) -> str:
    fd, path = tempfile.mkstemp(suffix=".webm")
    try:
        with os.fdopen(fd, 'wb') as f:
            f.write(audio_bytes)
        
        segments, _ = model.transcribe(path, beam_size=1)
        text = " ".join([segment.text for segment in segments])
        return text.strip()
    finally:
        os.remove(path)

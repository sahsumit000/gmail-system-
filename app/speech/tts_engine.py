import os
import tempfile
import asyncio
import edge_tts

async def generate_speech(text: str) -> str:
    voice = "en-US-ChristopherNeural"
    communicate = edge_tts.Communicate(text, voice)
    
    fd, path = tempfile.mkstemp(suffix=".mp3")
    os.close(fd)
    
    await communicate.save(path)
    return path

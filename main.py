from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
import edge_tts
import io
import asyncio

app = FastAPI()

class TTSRequest(BaseModel):
    text: str
    voice: str = "en-US-MichelleNeural"

@app.get("/")
async def root():
    return {"status": "Mai TTS server is running"}

@app.post("/tts")
async def tts(request: TTSRequest):
    communicate = edge_tts.Communicate(request.text, request.voice)
    audio_buffer = io.BytesIO()
    
    async for chunk in communicate.stream():
        if chunk["type"] == "audio":
            audio_buffer.write(chunk["data"])
    
    audio_buffer.seek(0)
    
    return StreamingResponse(
        audio_buffer,
        media_type="audio/mpeg",
        headers={"Content-Disposition": "attachment; filename=speech.mp3"}
    )
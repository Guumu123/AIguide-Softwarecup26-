from pydantic import BaseModel, Field
from typing import List, Optional, Dict

class ChatRequest(BaseModel):
    user_id: str
    message: str

class ChatResponse(BaseModel):
    text: str
    audio_url: Optional[str] = None
    emotion: str
    intensity: float
    debug: Optional[Dict] = None

class VoiceResponse(ChatResponse):
    pass

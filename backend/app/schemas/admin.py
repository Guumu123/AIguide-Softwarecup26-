from pydantic import BaseModel
from typing import List, Optional, Dict
from datetime import datetime

class AdminLoginRequest(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class StatsSummary(BaseModel):
    total_users: int
    active_users: int
    avg_satisfaction: float
    sentiment_distribution: Dict[str, int]

class KBUploadResponse(BaseModel):
    document_id: int
    status: str

class FAQCreate(BaseModel):
    question: str
    answer: str
    category: Optional[str] = None

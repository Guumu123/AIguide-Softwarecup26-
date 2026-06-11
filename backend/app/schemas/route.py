from pydantic import BaseModel
from typing import List, Optional, Dict

class RouteRecommendRequest(BaseModel):
    user_id: str
    age: int
    gender: str
    group_size: int
    interests: List[str]

class AttractionPoint(BaseModel):
    attraction_id: str
    name: str
    duration: str
    order: int
    highlights: str

class RouteRecommendResponse(BaseModel):
    route: List[AttractionPoint]
    total_duration: str
    estimated_cost: Dict[str, float]
    speech_highlights: Dict[str, str]
    speech_style: str
    tips: str

class AttractionDetail(BaseModel):
    id: str
    name: str
    description: str
    tips: str
    speech: str

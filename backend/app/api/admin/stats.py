from fastapi import APIRouter, Depends
from app.schemas.admin import StatsSummary
from app.core.dependencies import get_current_admin

router = APIRouter()

@router.get('/', response_model=StatsSummary, dependencies=[Depends(get_current_admin)])
async def get_stats():
    return {
        "total_users": 1250,
        "active_users": 45,
        "avg_satisfaction": 4.8,
        "sentiment_distribution": {
            "happy": 850,
            "neutral": 300,
            "sad": 100
        }
    }

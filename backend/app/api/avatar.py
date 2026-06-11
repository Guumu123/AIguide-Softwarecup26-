from fastapi import APIRouter
from typing import List, Dict

router = APIRouter()

@router.get('/config')
async def get_avatar_config(user_id: str):
    return {
        "user_id": user_id,
        "costume": "default",
        "voice": "sweet",
        "theme": "light",
        "style": "cartoon"
    }

@router.post('/config')
async def update_avatar_config(config: Dict):
    return {"status": "success", "updated_config": config}

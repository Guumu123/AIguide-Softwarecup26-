from fastapi import APIRouter, Query
from typing import List

router = APIRouter()

@router.get('/list')
async def list_attractions(scenic_area: str = Query(..., description="景区名称")):
    # 模拟返回景点列表
    return [
        {"id": "LS-001", "name": "灵山大佛", "scenic_area": scenic_area},
        {"id": "LS-002", "name": "九龙灌浴", "scenic_area": scenic_area},
        {"id": "LS-003", "name": "灵山梵宫", "scenic_area": scenic_area},
        {"id": "LS-004", "name": "五印坛城", "scenic_area": scenic_area},
    ]

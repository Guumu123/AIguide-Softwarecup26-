from fastapi import APIRouter, Depends, HTTPException
from app.schemas.route import RouteRecommendRequest, RouteRecommendResponse, AttractionDetail
from app.services.route_service import route_service
from typing import List

router = APIRouter()

# 模拟景点数据库
_attraction_db = {
    "LS-001": {
        "name": "灵山大佛",
        "description": "灵山大佛坐落于无锡马山秦履峰南侧。",
        "tips": "建议预留1小时游览，拍照最佳位置在佛手广场。",
        "speech": "各位游客，现在我们看到的是举世闻名的灵山大佛..."
    },
    "LS-002": {
        "name": "九龙灌浴",
        "description": "九龙灌浴再现佛祖诞生之祥瑞景象。",
        "tips": "注意演出时间表，建议提前10分钟占位。",
        "speech": "各位游客，九龙灌浴是灵山胜境最具震撼力的动态演出..."
    },
    "LS-003": {
        "name": "灵山梵宫",
        "description": "灵山梵宫汇聚东阳木雕、琉璃壁画等艺术瑰宝。",
        "tips": "殿内请勿大声喧哗，禁止拍照区域请遵守。",
        "speech": "各位游客，现在进入的是世界佛教论坛永久会址灵山梵宫..."
    },
}

@router.post('/recommend', response_model=RouteRecommendResponse)
async def recommend_route(request: RouteRecommendRequest):
    return route_service.recommend(request)

@router.get('/detail/{id}', response_model=AttractionDetail)
async def get_route_detail(id: str):
    attraction = _attraction_db.get(id)
    if not attraction:
        raise HTTPException(status_code=404, detail=f"景点 {id} 不存在")
    return {"id": id, **attraction}

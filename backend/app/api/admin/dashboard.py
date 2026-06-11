from fastapi import APIRouter, Depends, Query
from app.core.dependencies import get_current_admin
from typing import Optional
import random

router = APIRouter()

@router.get('/overview', dependencies=[Depends(get_current_admin)])
async def get_overview():
    return {
        "today_conversations": 1284,
        "active_users": 856,
        "satisfaction_score": 4.8,
        "avg_response_time": "0.8s",
        "total_routes_generated": 3120,
        "route_adoption_rate": 83.5,
        "today_voice_uploads": 645,
        "emotion_distribution": {
            "happy": 820, "neutral": 340, "sad": 124
        }
    }

@router.get('/trend', dependencies=[Depends(get_current_admin)])
async def get_trend(days: int = Query(7, ge=1, le=30)):
    days_zh = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"]
    data = []
    for i in range(days):
        data.append({
            "date": f"5-{14 + i}",
            "day": days_zh[i % 7],
            "conversations": 800 + random.randint(-200, 400),
            "active_users": 500 + random.randint(-100, 200),
            "satisfaction": round(4.5 + random.random() * 0.5, 1),
            "positive_pct": 55 + random.randint(-10, 15),
            "neutral_pct": 25 + random.randint(-5, 10),
            "negative_pct": 5 + random.randint(0, 10),
        })
    return {"days": days, "trend": data}

@router.get('/hot-routes', dependencies=[Depends(get_current_admin)])
async def get_hot_routes():
    return [
        {"rank": 1, "name": "灵山大佛深度游", "usage": 452, "rating": 4.8, "trend": 12},
        {"rank": 2, "name": "梵宫艺术之旅", "usage": 385, "rating": 4.9, "trend": -3},
        {"rank": 3, "name": "九龙灌浴祈福线", "usage": 312, "rating": 4.7, "trend": 8},
        {"rank": 4, "name": "五印坛城文化线", "usage": 256, "rating": 4.6, "trend": 5},
        {"rank": 5, "name": "祥符禅寺古迹线", "usage": 198, "rating": 4.5, "trend": 15},
    ]

@router.get('/hot-questions', dependencies=[Depends(get_current_admin)])
async def get_hot_questions():
    return [
        {"rank": 1, "question": "九龙灌浴表演时间？", "count": 452},
        {"rank": 2, "question": "怎么去梵宫？", "count": 385},
        {"rank": 3, "question": "灵山大佛门票多少钱？", "count": 312},
        {"rank": 4, "question": "哪里有素斋？", "count": 256},
        {"rank": 5, "question": "怎么租借轮椅？", "count": 198},
        {"rank": 6, "question": "梵宫几点关门？", "count": 156},
        {"rank": 7, "question": "有没有行李寄存？", "count": 128},
        {"rank": 8, "question": "怎么预约讲解？", "count": 98},
        {"rank": 9, "question": "景区有摆渡车吗？", "count": 86},
        {"rank": 10, "question": "怎么去五印坛城？", "count": 64},
    ]

@router.get('/recent-feedback', dependencies=[Depends(get_current_admin)])
async def get_recent_feedback():
    return [
        {"content": "讲解非常详细，声音好听", "timestamp": "2024-05-20 10:30", "type": "success"},
        {"content": "九龙灌浴时间提醒很准确", "timestamp": "2024-05-20 09:45", "type": "primary"},
        {"content": "希望能增加更多互动内容", "timestamp": "2024-05-20 09:15", "type": "warning"},
        {"content": "梵宫内部导航有点迷路", "timestamp": "2024-05-19 16:20", "type": "danger"},
        {"content": "路线推荐很符合我的兴趣", "timestamp": "2024-05-19 15:00", "type": "success"},
        {"content": "素斋味道不错价格合理", "timestamp": "2024-05-19 12:30", "type": "primary"},
    ]

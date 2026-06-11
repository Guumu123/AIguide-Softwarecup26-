from fastapi import APIRouter, Depends, Query
from app.core.dependencies import get_current_admin
from typing import Optional

router = APIRouter()

@router.get('/sentiment', dependencies=[Depends(get_current_admin)])
async def get_sentiment_report(date: Optional[str] = Query(None)):
    """游客感受度报告"""
    return {
        "date": date or "2024-05-20",
        "total_conversations": 1256,
        "sentiment_dist": {
            "positive": 65,
            "neutral": 25,
            "negative": 10
        },
        "satisfaction_score": 4.8,
        "hot_topics": [
            {"topic": "九龙灌浴表演时间", "count": 452, "trend": 12},
            {"topic": "梵宫门票预约", "count": 385, "trend": -5},
            {"topic": "素斋位置", "count": 312, "trend": 8},
            {"topic": "灵山大佛高度", "count": 256, "trend": 2},
            {"topic": "轮椅租赁", "count": 198, "trend": 15},
            {"topic": "行李寄存", "count": 165, "trend": -3},
            {"topic": "摆渡车路线", "count": 142, "trend": 6},
            {"topic": "五印坛城", "count": 128, "trend": -8},
            {"topic": "讲解预约", "count": 112, "trend": 3},
            {"topic": "祥符禅寺", "count": 95, "trend": 1},
        ],
        "word_cloud_data": [
            {"name": "九龙灌浴", "value": 452},
            {"name": "梵宫", "value": 385},
            {"name": "灵山大佛", "value": 312},
            {"name": "素斋", "value": 256},
            {"name": "门票", "value": 198},
            {"name": "轮椅", "value": 165},
            {"name": "行李", "value": 142},
            {"name": "摆渡车", "value": 128},
            {"name": "讲解", "value": 112},
            {"name": "禅寺", "value": 95},
            {"name": "路线", "value": 82},
            {"name": "表演", "value": 76},
        ],
        "trend_data": {
            "dates": ["5-14", "5-15", "5-16", "5-17", "5-18", "5-19", "5-20"],
            "positive": [60, 62, 65, 63, 68, 70, 65],
            "neutral": [30, 28, 25, 27, 22, 20, 25],
            "negative": [10, 10, 10, 10, 10, 10, 10]
        },
        "service_suggestions": [
            {
                "issue": "多名游客反馈九龙灌浴排队时间长",
                "action": "建议增加表演场次或提前广播提示，引导游客分散入场",
                "priority": "高",
                "expected_impact": "预计减少30%排队投诉"
            },
            {
                "issue": "梵宫内部导览指示不够清晰",
                "action": "建议在关键岔路口增设指示牌，并在数字人导航中增加实时位置指引",
                "priority": "中",
                "expected_impact": "预计减少50%迷路求助"
            },
            {
                "issue": "关于景区文史背景的深度提问增加",
                "action": "建议丰富知识库中的历史文化分块内容，增加典故故事",
                "priority": "高",
                "expected_impact": "提升知识库覆盖率至95%"
            },
            {
                "issue": "周末餐饮排队时间过长",
                "action": "建议引入分时段预约用餐机制，增设临时用餐点",
                "priority": "中",
                "expected_impact": "预计缩短平均等待时间15分钟"
            },
        ]
    }

@router.get('/realtime', dependencies=[Depends(get_current_admin)])
async def get_realtime_data():
    """数据大屏实时数据"""
    import random
    from datetime import datetime
    return {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "today_visitors": 2840,
        "today_conversations": 1284,
        "today_routes": 452,
        "real_time_sentiment": {
            "current": "happy" if random.random() > 0.3 else "neutral",
            "recent_10": [random.choice(["happy", "neutral", "sad"]) for _ in range(10)]
        },
        "hot_qa": [
            {"question": "九龙灌浴表演时间？", "count": 452},
            {"question": "怎么去梵宫？", "count": 385},
            {"question": "灵山大佛门票多少钱？", "count": 312},
            {"question": "哪里有素斋？", "count": 256},
            {"question": "怎么租借轮椅？", "count": 198},
            {"question": "梵宫几点关门？", "count": 156},
            {"question": "有没有行李寄存？", "count": 128},
            {"question": "怎么预约讲解？", "count": 98},
            {"question": "景区有摆渡车吗？", "count": 86},
            {"question": "怎么去五印坛城？", "count": 64},
        ],
        "live_feed": [
            {"time": "14:30:15", "user": "User_827", "content": "九龙灌浴表演时间？", "sentiment": "happy"},
            {"time": "14:30:08", "user": "User_156", "content": "梵宫怎么走？", "sentiment": "neutral"},
            {"time": "14:29:55", "user": "User_334", "content": "素斋排队好长...", "sentiment": "sad"},
            {"time": "14:29:42", "user": "User_098", "content": "大佛好壮观！", "sentiment": "happy"},
            {"time": "14:29:30", "user": "User_762", "content": "怎么预约讲解？", "sentiment": "neutral"},
        ]
    }

from fastapi import APIRouter, Depends, Query
from app.core.dependencies import get_current_admin
from typing import Optional
from datetime import datetime, timedelta
import random

router = APIRouter()

_SAMPLE_MESSAGES = [
    "九龙灌浴表演时间是什么时候？",
    "怎么去灵山大佛？",
    "梵宫现在人多吗？",
    "附近有吃饭的地方吗？",
    "灵山大佛有多高？",
    "门票多少钱？",
    "有轮椅可以租吗？",
    "梵宫几点关门？",
    "哪里可以寄存行李？",
    "景区有摆渡车吗？",
]
_SAMPLE_RESPONSES = [
    "九龙灌浴每天有两场表演：上午10:00和下午15:00，建议提前10分钟占位。",
    "沿景区中轴线直行约500米即到灵山大佛，途中经过百子戏弥勒和降魔壁。",
    "目前梵宫游客较多，建议先游览五印坛城，稍后前往梵宫。",
    "景区内设有灵山蔬食馆，提供素斋，位于九龙灌浴东侧200米处。",
    "灵山大佛通高88米，佛体79米，莲花瓣9米，含台基总高101.5米。",
    "成人票210元，学生及老人半价，可在小程序提前预约。",
    "景区入口处提供轮椅租赁服务，押金200元。",
    "夏季开放至18:00，冬季至17:00，建议提前1小时入园。",
    "景区游客中心提供行李寄存柜，大件行李可寄存于服务台。",
    "景区提供免费接驳车，循环发车，间隔约15分钟。",
]

def _gen_mock_conversations(date_from: str = None, date_to: str = None, sentiment: str = None, voice_emotion: str = None):
    emotions = ["积极", "中性", "消极"]
    voice_emotions = ["happy", "neutral", "sad"]
    final_emotions = ["happy", "neutral", "sad"]
    data = []
    for i in range(30):
        ts = datetime.now() - timedelta(minutes=i * 12, days=i % 3)
        emo = emotions[i % 3]
        ve = voice_emotions[i % 3]
        fe = final_emotions[i % 3]
        if sentiment and emo != sentiment:
            continue
        if voice_emotion and ve != voice_emotion:
            continue
        data.append({
            "id": i + 1,
            "time": ts.strftime("%Y-%m-%d %H:%M:%S"),
            "user": f"User_{(i * 137) % 1000:03d}",
            "message": _SAMPLE_MESSAGES[i % len(_SAMPLE_MESSAGES)],
            "response": _SAMPLE_RESPONSES[i % len(_SAMPLE_RESPONSES)],
            "message_type": "text" if i % 3 else "voice",
            "text_sentiment": emo,
            "voice_sentiment": ve,
            "final_emotion": fe,
            "sentiment_intensity": round(0.5 + random.random() * 0.5, 2),
            "text_confidence": round(0.7 + random.random() * 0.3, 2),
        })
    return data

@router.get('/', dependencies=[Depends(get_current_admin)])
async def list_conversations(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    sentiment: Optional[str] = Query(None),
    voice_emotion: Optional[str] = Query(None),
    date_from: Optional[str] = Query(None),
    date_to: Optional[str] = Query(None),
):
    all_data = _gen_mock_conversations(date_from, date_to, sentiment, voice_emotion)
    total = len(all_data)
    start = (page - 1) * page_size
    end = start + page_size
    return {
        "total": total,
        "page": page,
        "page_size": page_size,
        "items": all_data[start:end]
    }

@router.get('/{conversation_id}', dependencies=[Depends(get_current_admin)])
async def get_conversation_detail(conversation_id: int):
    all_data = _gen_mock_conversations()
    for item in all_data:
        if item["id"] == conversation_id:
            return item
    return {"error": "对话不存在"}

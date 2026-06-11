"""WebSocket 实时数据推送 - 数据大屏"""
import asyncio
import json
import random
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from typing import Optional

router = APIRouter()


class DashboardBroadcaster:
    def __init__(self):
        self._connections: list[WebSocket] = []

    async def connect(self, ws: WebSocket):
        await ws.accept()
        self._connections.append(ws)

    def disconnect(self, ws: WebSocket):
        self._connections.remove(ws)

    async def broadcast(self, data: dict):
        disconnected = []
        for ws in self._connections:
            try:
                await ws.send_json(data)
            except Exception:
                disconnected.append(ws)
        for ws in disconnected:
            self.disconnect(ws)

    @property
    def active_count(self) -> int:
        return len(self._connections)


broadcaster = DashboardBroadcaster()

_HOT_QUESTIONS = [
    "九龙灌浴表演时间？", "怎么去梵宫？", "灵山大佛门票多少钱？",
    "哪里有素斋？", "怎么租借轮椅？", "梵宫几点关门？",
    "有没有行李寄存？", "怎么写预约讲解？", "景区有摆渡车吗？",
    "怎么去五印坛城？",
]
_USER_NAMES = ["User_827", "User_156", "User_334", "User_098", "User_762", "User_215", "User_643"]


async def _emit_live_feed():
    """后台任务：每 3 秒推送一条模拟实时对话"""
    while True:
        await asyncio.sleep(3)
        if broadcaster.active_count == 0:
            continue
        msg = {
            "time": f"14:{random.randint(0, 59):02d}:{random.randint(0, 59):02d}",
            "user": random.choice(_USER_NAMES),
            "content": random.choice(_HOT_QUESTIONS),
            "sentiment": random.choice(["happy", "happy", "happy", "neutral", "sad"]),
        }
        await broadcaster.broadcast({"type": "live_feed", "data": msg})


@router.websocket("/realtime")
async def dashboard_websocket(ws: WebSocket):
    await broadcaster.connect(ws)
    try:
        # 首次推送全量数据
        await ws.send_json({
            "type": "snapshot",
            "data": {
                "today_conversations": 1284,
                "active_users": 856,
                "satisfaction_score": 4.8,
                "hot_questions": [{"rank": i+1, "question": q, "count": random.randint(80, 500)}
                                  for i, q in enumerate(_HOT_QUESTIONS)],
                "emotion_distribution": {"happy": 820, "neutral": 340, "sad": 124},
            }
        })

        # 持续接收心跳并推送实时数据
        while True:
            try:
                data = await asyncio.wait_for(ws.receive_text(), timeout=60)
                if data == "ping":
                    await ws.send_json({"type": "pong"})
            except asyncio.TimeoutError:
                # 超时发送心跳
                await ws.send_json({"type": "heartbeat"})
    except WebSocketDisconnect:
        pass
    finally:
        broadcaster.disconnect(ws)

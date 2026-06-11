from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.api import chat, voice, route, avatar, attractions
from app.api.admin import auth, avatar as admin_avatar, stats, conversations, insights, kb, reports, dashboard, ws
from app.core.cache import cache_manager
from app.services.scheduler import report_scheduler

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url="/openapi.json",
    docs_url="/docs",
    redoc_url="/redoc",
)

# Set all CORS enabled origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Tourist Routes
app.include_router(chat.router, prefix="/chat", tags=["Tourist - Chat"])
app.include_router(voice.router, prefix="/voice", tags=["Tourist - Voice"])
app.include_router(route.router, prefix="/route", tags=["Tourist - Route"])
app.include_router(avatar.router, prefix="/avatar", tags=["Tourist - Avatar"])
app.include_router(attractions.router, prefix="/attractions", tags=["Tourist - Attractions"])

# Admin Routes
app.include_router(auth.router, prefix="/admin", tags=["Admin - Auth"])
app.include_router(stats.router, prefix="/admin/stats", tags=["Admin - Stats"])
app.include_router(conversations.router, prefix="/admin/conversations", tags=["Admin - Conversations"])
app.include_router(insights.router, prefix="/admin/insights", tags=["Admin - Insights"])
app.include_router(kb.router, prefix="/admin/kb", tags=["Admin - Knowledge Base"])
app.include_router(admin_avatar.router, prefix="/admin/avatar", tags=["Admin - Avatar"])
app.include_router(reports.router, prefix="/admin/reports", tags=["Admin - Reports"])
app.include_router(dashboard.router, prefix="/admin/dashboard", tags=["Admin - Dashboard"])
app.include_router(ws.router, prefix="/ws", tags=["Admin - WebSocket"])


@app.on_event("startup")
async def startup():
    """启动时初始化缓存和调度器"""
    await cache_manager.init()
    await report_scheduler.start()


@app.on_event("shutdown")
async def shutdown():
    """关闭时清理资源"""
    await report_scheduler.stop()


@app.get("/")
async def root():
    return {"message": f"Welcome to {settings.PROJECT_NAME} API"}

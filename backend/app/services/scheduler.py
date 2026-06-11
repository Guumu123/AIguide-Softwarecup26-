"""APScheduler 定时任务 - 每日报告生成"""
import asyncio
from datetime import datetime


class ReportScheduler:
    """定时报告生成器（可接入 APScheduler 或手动 cron）"""

    def __init__(self):
        self._running = False
        self._task: asyncio.Task | None = None

    async def start(self):
        """启动定时任务循环"""
        if self._running:
            return
        self._running = True
        self._task = asyncio.create_task(self._daily_loop())
        print("[Scheduler] 日报定时任务已启动（每日凌晨 2:00）")

    async def stop(self):
        """停止定时任务"""
        self._running = False
        if self._task:
            self._task.cancel()

    async def _daily_loop(self):
        """主循环：等待到每日凌晨 2:00 执行"""
        while self._running:
            now = datetime.now()
            # 计算到下一个凌晨2点的秒数
            next_run = now.replace(hour=2, minute=0, second=0, microsecond=0)
            if now >= next_run:
                from datetime import timedelta
                next_run += timedelta(days=1)
            wait_seconds = (next_run - now).total_seconds()
            await asyncio.sleep(wait_seconds)

            try:
                report = await self._generate_daily_report()
                print(f"[Scheduler] 日报已生成: {report['date']}, "
                      f"对话数={report['total_conversations']}, "
                      f"满意度={report['satisfaction_score']}")
            except Exception as e:
                print(f"[Scheduler] 日报生成失败: {e}")

    async def _generate_daily_report(self) -> dict:
        """生成每日游客感受度报告"""
        today = datetime.now().strftime("%Y-%m-%d")
        return {
            "date": today,
            "total_conversations": 0,
            "total_routes": 0,
            "satisfaction_score": 0.0,
            "sentiment_dist": {"positive": 0, "neutral": 0, "negative": 0},
            "hot_topics": [],
            "generated_at": datetime.now().isoformat(),
        }

    async def trigger_now(self) -> dict:
        """手动触发一次报告生成（调试用）"""
        return await self._generate_daily_report()


# 全局实例
report_scheduler = ReportScheduler()

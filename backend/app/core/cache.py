"""Redis 缓存服务 - 支持真实 Redis 和内存降级"""
import json
import time
import asyncio
from typing import Optional, Any
from app.config import settings


class InMemoryCache:
    """内存缓存降级实现（当 Redis 不可用时）"""
    def __init__(self):
        self._store: dict[str, tuple[Any, float]] = {}

    async def get(self, key: str) -> Optional[Any]:
        if key in self._store:
            val, expire_at = self._store[key]
            if expire_at > time.time() or expire_at == 0:
                return val
            del self._store[key]
        return None

    async def set(self, key: str, value: Any, ttl: int = 0):
        expire_at = time.time() + ttl if ttl > 0 else 0
        self._store[key] = (value, expire_at)

    async def delete(self, key: str):
        self._store.pop(key, None)

    async def incr(self, key: str) -> int:
        val = await self.get(key) or 0
        val += 1
        await self.set(key, val)
        return val


class RedisCache:
    """Redis 缓存封装，自动降级到内存缓存"""
    def __init__(self):
        self._using_redis = False
        self._redis = None
        self._fallback = InMemoryCache()

    async def init(self):
        try:
            import redis.asyncio as aioredis
            self._redis = await aioredis.from_url(
                settings.REDIS_URL,
                encoding="utf-8",
                decode_responses=True,
                socket_connect_timeout=2,
                socket_timeout=2,
            )
            await self._redis.ping()
            self._using_redis = True
            print(f"[Cache] Using Redis at {settings.REDIS_URL}")
        except Exception as e:
            print(f"[Cache] Redis unavailable ({e}), using in-memory fallback")
            self._using_redis = False

    async def get(self, key: str) -> Optional[Any]:
        if self._using_redis:
            try:
                val = await self._redis.get(key)
                if val:
                    return json.loads(val)
                return None
            except Exception:
                self._using_redis = False
        return await self._fallback.get(key)

    async def set(self, key: str, value: Any, ttl: int = 0):
        if self._using_redis:
            try:
                await self._redis.set(key, json.dumps(value, ensure_ascii=False), ex=ttl if ttl > 0 else None)
                return
            except Exception:
                self._using_redis = False
        await self._fallback.set(key, value, ttl)

    async def delete(self, key: str):
        if self._using_redis:
            try:
                await self._redis.delete(key)
                return
            except Exception:
                self._using_redis = False
        await self._fallback.delete(key)

    async def incr(self, key: str) -> int:
        if self._using_redis:
            try:
                return await self._redis.incr(key)
            except Exception:
                self._using_redis = False
        return await self._fallback.incr(key)

    @property
    def using_redis(self) -> bool:
        return self._using_redis


# 全局实例
cache_manager = RedisCache()

"""Feature flag access abstraction with Redis async fallback to in-memory dict."""
from typing import Optional
import os

_IN_MEM: dict[str, dict] = {}

REDIS_URL = os.environ.get("REDIS_URL") or os.environ.get("AI_AGENT_REDIS_URL")


class FeatureFlags:
    def __init__(self):
        self._redis = None
        # try to import redis.asyncio when available
        try:
            import redis.asyncio as aioredis  # type: ignore

            self._aioredis = aioredis.from_url(REDIS_URL) if REDIS_URL else None
        except Exception:
            self._aioredis = None

    async def get_flag(self, tenant_id: str, flag: str) -> Optional[bool]:
        key = f"tenant:{tenant_id}:flag:{flag}"
        if self._aioredis:
            try:
                v = await self._aioredis.get(key)
                if v is None:
                    return None
                return v.decode("utf-8") in ("1", "true", "True")
            except Exception:
                return None

        # fallback to in-memory
        return _IN_MEM.get(tenant_id, {}).get(flag)

    async def set_flag(self, tenant_id: str, flag: str, value: bool) -> None:
        key = f"tenant:{tenant_id}:flag:{flag}"
        if self._aioredis:
            try:
                await self._aioredis.set(key, "1" if value else "0")
                return
            except Exception:
                pass

        if tenant_id not in _IN_MEM:
            _IN_MEM[tenant_id] = {}
        _IN_MEM[tenant_id][flag] = bool(value)


feature_flags = FeatureFlags()

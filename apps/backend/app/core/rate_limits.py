import time
from collections import defaultdict, deque
from threading import Lock


class RateLimitExceeded(Exception):
    def __init__(self, retry_after_seconds: int, detail: str = "Rate limit exceeded") -> None:
        self.retry_after_seconds = retry_after_seconds
        self.detail = detail
        super().__init__(detail)


class InMemoryRateLimiter:
    def __init__(self) -> None:
        self._buckets: dict[str, deque[float]] = defaultdict(deque)
        self._lock = Lock()

    def check(self, key: str, max_requests: int, window_seconds: int) -> int | None:
        now = time.time()
        cutoff = now - window_seconds

        with self._lock:
            bucket = self._buckets[key]
            while bucket and bucket[0] <= cutoff:
                bucket.popleft()

            if len(bucket) >= max_requests:
                retry_after = int(max(1, window_seconds - (now - bucket[0])))
                return retry_after

            bucket.append(now)
            return None


rate_limiter = InMemoryRateLimiter()

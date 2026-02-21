from __future__ import annotations

import functools
import time


def retry(func=None, *, max_attempts: int = 3, delay: float = 1.0, backoff: float = 2.0):
    def decorator(inner):
        @functools.wraps(inner)
        def wrapper(*args, **kwargs):
            attempts = 0
            wait = delay
            while True:
                attempts += 1
                try:
                    return inner(*args, **kwargs)
                except Exception:
                    if attempts >= max_attempts:
                        raise
                    time.sleep(wait)
                    wait *= backoff

        return wrapper

    return decorator(func) if func else decorator

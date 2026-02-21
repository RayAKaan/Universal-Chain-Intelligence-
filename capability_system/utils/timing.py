from __future__ import annotations

import logging
import time
from contextlib import ContextDecorator


def timed(func):
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        out = func(*args, **kwargs)
        elapsed = (time.perf_counter() - start) * 1000
        logging.getLogger(func.__module__).info("%s took %.2fms", func.__name__, elapsed)
        return out

    return wrapper


class Timer(ContextDecorator):
    def __enter__(self):
        self.start = time.perf_counter()
        self.elapsed_ms = 0.0
        return self

    def __exit__(self, exc_type, exc, tb):
        self.elapsed_ms = (time.perf_counter() - self.start) * 1000
        return False

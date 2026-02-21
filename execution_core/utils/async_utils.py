"""Async helper functions for bridging sync and async execution."""

from __future__ import annotations

import asyncio
from functools import partial
from typing import Any, Callable


async def run_sync_in_thread(func: Callable[..., Any], *args: Any, **kwargs: Any) -> Any:
    """Run blocking work in a default thread pool without blocking loop."""
    loop = asyncio.get_running_loop()
    bound = partial(func, *args, **kwargs)
    return await loop.run_in_executor(None, bound)


def ensure_event_loop() -> asyncio.AbstractEventLoop:
    """Get or create an event loop for current thread."""
    try:
        return asyncio.get_running_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        return loop

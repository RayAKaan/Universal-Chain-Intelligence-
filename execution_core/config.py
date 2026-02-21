"""Configuration values for deterministic execution core."""

from dataclasses import dataclass


@dataclass(frozen=True)
class EngineConfig:
    max_workers: int = 4
    max_queue_size: int = 0  # 0 means unbounded for PriorityQueue
    default_timeout_seconds: int = 60
    scheduler_poll_interval: float = 0.05
    thread_name_prefix: str = "uci-exec"


DEFAULT_CONFIG = EngineConfig()

from __future__ import annotations

import statistics


def calculate_percentile(samples: list[float], percentile: float) -> float:
    if not samples:
        return 0.0
    samples = sorted(samples)
    idx = max(0, min(len(samples) - 1, int((percentile / 100.0) * (len(samples) - 1))))
    return samples[idx]


def calculate_latency_stats(samples: list[float]) -> dict:
    if not samples:
        return {k: 0.0 for k in ["avg", "p50", "p95", "p99", "min", "max", "std_dev"]}
    return {
        "avg": statistics.mean(samples),
        "p50": calculate_percentile(samples, 50),
        "p95": calculate_percentile(samples, 95),
        "p99": calculate_percentile(samples, 99),
        "min": min(samples),
        "max": max(samples),
        "std_dev": statistics.pstdev(samples) if len(samples) > 1 else 0.0,
    }


def calculate_throughput(samples: list[float], duration: float) -> float:
    return (len(samples) / duration) if duration > 0 else 0.0


def calculate_reliability(success: int, total: int) -> float:
    return success / total if total else 0.0


def detect_outliers(samples: list[float]) -> list[float]:
    if len(samples) < 4:
        return []
    q1 = calculate_percentile(samples, 25)
    q3 = calculate_percentile(samples, 75)
    iqr = q3 - q1
    low, high = q1 - 1.5 * iqr, q3 + 1.5 * iqr
    return [x for x in samples if x < low or x > high]


def calculate_trend(historical_results: list) -> str:
    if len(historical_results) < 2:
        return "stable"
    first = historical_results[0].avg_latency_ms
    last = historical_results[-1].avg_latency_ms
    if last < first * 0.95:
        return "improving"
    if last > first * 1.05:
        return "degrading"
    return "stable"

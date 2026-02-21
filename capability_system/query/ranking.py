from __future__ import annotations


def rank_by_latency(capabilities):
    return sorted(capabilities, key=lambda c: c.performance_profile.avg_latency_ms or float("inf"))


def rank_by_reliability(capabilities):
    return sorted(capabilities, key=lambda c: c.performance_profile.reliability, reverse=True)


def calculate_composite_score(capability, weights: dict) -> float:
    latency = capability.performance_profile.avg_latency_ms
    latency_score = 1.0 / (1.0 + max(latency, 0.0))
    reliability = capability.performance_profile.reliability
    accuracy = capability.performance_profile.accuracy
    throughput = capability.performance_profile.throughput_per_second
    throughput_score = throughput / (throughput + 1.0)
    return (
        weights.get("latency", 0.3) * latency_score
        + weights.get("reliability", 0.3) * reliability
        + weights.get("accuracy", 0.2) * accuracy
        + weights.get("throughput", 0.2) * throughput_score
    )


def rank_by_composite_score(capabilities, weights: dict | None = None):
    weights = weights or {"latency": 0.3, "reliability": 0.3, "accuracy": 0.2, "throughput": 0.2}
    return sorted(capabilities, key=lambda c: calculate_composite_score(c, weights), reverse=True)

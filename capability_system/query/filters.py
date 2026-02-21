from __future__ import annotations


def filter_by_type(capabilities, cap_type):
    return [c for c in capabilities if c.capability_type == cap_type]


def filter_by_category(capabilities, category):
    return [c for c in capabilities if c.category == category]


def filter_by_health(capabilities, health):
    return [c for c in capabilities if c.health_status == health]


def filter_by_performance(capabilities, min_reliability=None, max_latency=None):
    out = capabilities
    if min_reliability is not None:
        out = [c for c in out if c.performance_profile.reliability >= min_reliability]
    if max_latency is not None:
        out = [c for c in out if c.performance_profile.avg_latency_ms <= max_latency]
    return out


def filter_by_tags(capabilities, tags, match_all=False):
    tags = set(tags)
    if match_all:
        return [c for c in capabilities if tags.issubset(set(c.metadata.get("tags", [])))]
    return [c for c in capabilities if set(c.metadata.get("tags", [])) & tags]


def apply_filters(capabilities, filters: dict):
    out = list(capabilities)
    if "type" in filters:
        out = filter_by_type(out, filters["type"])
    if "category" in filters:
        out = filter_by_category(out, filters["category"])
    if "health" in filters:
        out = filter_by_health(out, filters["health"])
    if "min_reliability" in filters or "max_latency_ms" in filters:
        out = filter_by_performance(out, filters.get("min_reliability"), filters.get("max_latency_ms"))
    if "tags" in filters:
        out = filter_by_tags(out, filters["tags"], filters.get("match_all_tags", False))
    if "is_enabled" in filters:
        out = [c for c in out if c.is_enabled == filters["is_enabled"]]
    if "state" in filters:
        out = [c for c in out if c.state == filters["state"]]
    return out

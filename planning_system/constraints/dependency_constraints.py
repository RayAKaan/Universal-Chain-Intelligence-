from __future__ import annotations


def RequiredCapabilityConstraint(plan, capability_id):
    used = {s.capability_id for s in plan.steps}
    return capability_id in used, used


def ExcludedCapabilityConstraint(plan, capability_id):
    used = {s.capability_id for s in plan.steps}
    return capability_id not in used, used


def OrderConstraint(plan, order_pair):
    a, b = order_pair
    idx = {s.name: i for i, s in enumerate(plan.steps)}
    return idx.get(a, -1) < idx.get(b, 10**9), idx

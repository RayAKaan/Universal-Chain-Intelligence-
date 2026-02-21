from __future__ import annotations


def calculate_critical_path(graph):
    return [n.node_id for n in graph.get_critical_path()]


def calculate_slack(graph):
    cp = set(calculate_critical_path(graph))
    return {n.node_id: 0.0 if n.node_id in cp else 1.0 for n in graph}


def find_bottlenecks(graph):
    cp = calculate_critical_path(graph)
    return [n for n in cp if graph.nodes[n].step.estimated_duration_ms > 5000]


def calculate_resource_timeline(graph):
    levels = graph.get_execution_levels()
    tl = []
    t = 0.0
    for lvl in levels:
        cpu = sum(getattr(getattr(n.step, "resource_requirements", None), "min_cpu_cores", 0.1) if n.step.resource_requirements else 0.1 for n in lvl)
        mem = sum(getattr(getattr(n.step, "resource_requirements", None), "min_memory_mb", 64) if n.step.resource_requirements else 64 for n in lvl)
        tl.append({"time": t, "cpu": cpu, "memory_mb": mem})
        t += max((n.step.estimated_duration_ms for n in lvl), default=0)
    return tl


def estimate_total_duration(graph, parallel=True):
    return graph.get_parallel_estimated_duration() if parallel else graph.get_total_estimated_duration()


def find_independent_chains(graph):
    return [[n.node_id for n in lvl] for lvl in graph.get_execution_levels()]


def get_execution_order(graph):
    return [[n.node_id for n in lvl] for lvl in graph.get_execution_levels()]

from __future__ import annotations


def visualize_text(graph) -> str:
    lines = ["Execution DAG"]
    for n in graph.topological_sort():
        succ = ",".join(graph.nodes[n.node_id].outgoing_edges) or "-"
        lines.append(f"- {n.step.name} [{n.step.status}] -> {succ}")
    lines.append("Critical path: " + " -> ".join(x.step.name for x in graph.get_critical_path()))
    return "\n".join(lines)


def visualize_timeline(graph) -> str:
    lines = ["Timeline"]
    t = 0
    for lvl in graph.get_execution_levels():
        names = ", ".join(n.step.name for n in lvl)
        dur = max((n.step.estimated_duration_ms for n in lvl), default=0)
        lines.append(f"t={t:.0f}ms | {names} | +{dur:.0f}ms")
        t += dur
    return "\n".join(lines)


def visualize_status(graph) -> str:
    total = len(graph.nodes)
    done = len([n for n in graph if n.step.status == "COMPLETED"])
    pct = int((done / total) * 100) if total else 0
    bar = "■" * (pct // 10) + "□" * (10 - pct // 10)
    running = [n.step.name for n in graph if n.step.status == "RUNNING"]
    nextn = [n.step.name for n in graph.get_ready_nodes()]
    return f"[{bar}] {pct}% complete ({done}/{total})\nRunning: {', '.join(running) or '-'}\nNext: {', '.join(nextn) or '-'}"


def export_dot(graph) -> str:
    lines = ["digraph Plan {"]
    for nid, n in graph.nodes.items():
        lines.append(f'  "{nid}" [label="{n.step.name}"];')
    for a, b in graph.edges:
        lines.append(f'  "{a}" -> "{b}";')
    lines.append("}")
    return "\n".join(lines)

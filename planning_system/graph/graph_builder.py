from __future__ import annotations

from planning_system.graph.dependency_graph import ExecutionGraph
from planning_system.models.plan_node import PlanNode
from planning_system.models.plan_step import PlanStep, StepType


def infer_dependencies(steps: list[PlanStep]) -> list[tuple[str, str]]:
    edges = []
    by_id = {s.step_id: s for s in steps}
    for s in steps:
        for dep in s.dependencies:
            if dep in by_id:
                edges.append((dep, s.step_id))
        for src in s.input_mapping.values():
            if isinstance(src, dict) and src.get("source") == "step":
                edges.append((src["step_id"], s.step_id))
    return list(dict.fromkeys(edges))


def build_graph(task_tree, dependencies: list[tuple] | None = None) -> ExecutionGraph:
    g = ExecutionGraph()
    leaves = task_tree.get_leaves()
    for s in leaves:
        g.add_node(PlanNode(node_id=s.step_id, step=s))
    edges = infer_dependencies(leaves)
    if not edges:
        ordered = sorted(leaves, key=lambda x: x.name)
        for i in range(len(ordered) - 1):
            edges.append((ordered[i].step_id, ordered[i + 1].step_id))
    if dependencies:
        edges.extend(dependencies)
    for a, b in edges:
        if a in g.nodes and b in g.nodes and a != b:
            g.add_edge(a, b)
    if g.has_cycle():
        raise ValueError("graph contains cycle")
    return g


def add_checkpoint_nodes(graph: ExecutionGraph, interval: int = 5) -> ExecutionGraph:
    nodes = list(graph.nodes.values())
    for idx in range(interval, len(nodes), interval):
        cp = PlanStep(name=f"checkpoint_{idx}", description="checkpoint", step_type=StepType.CHECKPOINT)
        node = PlanNode(node_id=cp.step_id, step=cp)
        graph.add_node(node)
    return graph


def add_gate_nodes(graph: ExecutionGraph, gates: list[dict]) -> ExecutionGraph:
    for g in gates:
        step = PlanStep(name=g.get("name", "gate"), description="gate", step_type=StepType.GATE)
        node = PlanNode(node_id=step.step_id, step=step)
        graph.add_node(node)
    return graph

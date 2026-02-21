from __future__ import annotations

from collections import defaultdict

from planning_system.graph.topological_sort import detect_cycle, topological_sort
from planning_system.models.plan_node import PlanNode


class ExecutionGraph:
    def __init__(self):
        self.nodes: dict[str, PlanNode] = {}
        self.edges: list[tuple[str, str]] = []

    def add_node(self, node: PlanNode) -> None:
        self.nodes[node.node_id] = node

    def remove_node(self, node_id: str) -> None:
        self.nodes.pop(node_id, None)
        self.edges = [(a, b) for a, b in self.edges if a != node_id and b != node_id]

    def add_edge(self, from_id: str, to_id: str) -> None:
        if (from_id, to_id) not in self.edges:
            self.edges.append((from_id, to_id))
            self.nodes[from_id].outgoing_edges.append(to_id)
            self.nodes[to_id].incoming_edges.append(from_id)

    def remove_edge(self, from_id: str, to_id: str) -> None:
        if (from_id, to_id) in self.edges:
            self.edges.remove((from_id, to_id))

    def get_node(self, node_id: str) -> PlanNode:
        return self.nodes[node_id]

    def get_roots(self):
        return [n for n in self.nodes.values() if not n.incoming_edges]

    def get_leaves(self):
        return [n for n in self.nodes.values() if not n.outgoing_edges]

    def get_predecessors(self, node_id: str):
        return [self.nodes[x] for x in self.nodes[node_id].incoming_edges]

    def get_successors(self, node_id: str):
        return [self.nodes[x] for x in self.nodes[node_id].outgoing_edges]

    def has_cycle(self) -> bool:
        return bool(detect_cycle(self.nodes, self.edges))

    def topological_sort(self):
        return [self.nodes[i] for i in topological_sort(self.nodes, self.edges)]

    def get_ready_nodes(self):
        out = []
        for n in self.nodes.values():
            if n.step.status in {"PENDING", "READY", "BLOCKED"}:
                if all(self.nodes[p].step.status == "COMPLETED" for p in n.incoming_edges):
                    out.append(n)
        return out

    def mark_completed(self, node_id: str):
        self.nodes[node_id].step.status = "COMPLETED"
        self.nodes[node_id].is_completed = True
        return self.get_ready_nodes()

    def mark_failed(self, node_id: str):
        self.nodes[node_id].step.status = "FAILED"
        return [self.nodes[s] for s in self.nodes[node_id].outgoing_edges]

    def get_execution_levels(self):
        indeg = {n: len(self.nodes[n].incoming_edges) for n in self.nodes}
        levels = []
        ready = [n for n, d in indeg.items() if d == 0]
        while ready:
            lvl_nodes = [self.nodes[n] for n in ready]
            levels.append(lvl_nodes)
            nxt = []
            for n in ready:
                for s in self.nodes[n].outgoing_edges:
                    indeg[s] -= 1
                    if indeg[s] == 0:
                        nxt.append(s)
            ready = nxt
        return levels

    def get_parallelism_degree(self):
        return max((len(l) for l in self.get_execution_levels()), default=1)

    def get_critical_path(self):
        order = [n.node_id for n in self.topological_sort()]
        dist, prev = {n: 0.0 for n in self.nodes}, {}
        for n in order:
            for s in self.nodes[n].outgoing_edges:
                nd = dist[n] + self.nodes[n].step.estimated_duration_ms
                if nd > dist[s]:
                    dist[s], prev[s] = nd, n
        end = max(dist, key=dist.get) if dist else None
        path = []
        while end:
            path.append(self.nodes[end])
            end = prev.get(end)
        return list(reversed(path))

    def get_critical_path_duration(self):
        return sum(n.step.estimated_duration_ms for n in self.get_critical_path())

    def get_total_estimated_duration(self):
        return sum(n.step.estimated_duration_ms for n in self.nodes.values())

    def get_parallel_estimated_duration(self):
        return self.get_critical_path_duration()

    def subgraph(self, node_ids):
        g = ExecutionGraph()
        for nid in node_ids:
            if nid in self.nodes:
                g.add_node(self.nodes[nid])
        for a, b in self.edges:
            if a in g.nodes and b in g.nodes:
                g.add_edge(a, b)
        return g

    def merge(self, other):
        g = ExecutionGraph()
        for src in (self, other):
            for n in src.nodes.values():
                g.add_node(n)
            for a, b in src.edges:
                g.add_edge(a, b)
        return g

    def to_dict(self):
        return {"nodes": list(self.nodes.keys()), "edges": self.edges}

    @classmethod
    def from_dict(cls, data):
        g = cls()
        g.edges = [tuple(e) for e in data.get("edges", [])]
        return g

    def validate(self):
        issues = []
        if self.has_cycle():
            issues.append("cycles detected")
        for a, b in self.edges:
            if a not in self.nodes or b not in self.nodes:
                issues.append("invalid node references")
        return issues

    def __len__(self):
        return len(self.nodes)

    def __contains__(self, node_id):
        return node_id in self.nodes

    def __iter__(self):
        return iter(self.nodes.values())

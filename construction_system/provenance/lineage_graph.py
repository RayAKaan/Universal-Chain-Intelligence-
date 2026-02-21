from __future__ import annotations


class LineageGraph:
    def __init__(self):
        self.nodes = {}
        self.edges = []

    def add_record(self, r):
        self.nodes[r.record_id] = r
        for p in r.parent_artifacts:
            self.edges.append((p, r.artifact_id))

    def get_ancestors(self, artifact_id):
        return [a for a, b in self.edges if b == artifact_id]

    def get_descendants(self, artifact_id):
        return [b for a, b in self.edges if a == artifact_id]

    def get_root_artifacts(self):
        children = {b for _, b in self.edges}
        parents = {a for a, _ in self.edges}
        return list(parents - children)

    def to_dict(self):
        return {"nodes": list(self.nodes.keys()), "edges": self.edges}

    def visualize_text(self):
        return "\n".join(f"{a} -> {b}" for a, b in self.edges) or "(empty lineage)"

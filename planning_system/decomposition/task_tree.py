from __future__ import annotations

from dataclasses import asdict

from planning_system.models.plan_step import PlanStep


class TaskTree:
    def __init__(self, root: PlanStep):
        self.root = root
        self.nodes: dict[str, PlanStep] = {root.step_id: root}

    def add_step(self, step: PlanStep, parent_id: str | None = None) -> None:
        self.nodes[step.step_id] = step
        if parent_id:
            parent = self.nodes[parent_id]
            step.parent_step_id = parent_id
            step.level = parent.level + 1
            parent.child_step_ids.append(step.step_id)
            parent.is_leaf = False

    def remove_step(self, step_id: str) -> None:
        self.nodes.pop(step_id, None)

    def get_step(self, step_id: str) -> PlanStep:
        return self.nodes[step_id]

    def get_children(self, step_id: str) -> list[PlanStep]:
        return [self.nodes[c] for c in self.nodes[step_id].child_step_ids]

    def get_parent(self, step_id: str) -> PlanStep | None:
        pid = self.nodes[step_id].parent_step_id
        return self.nodes.get(pid) if pid else None

    def get_leaves(self) -> list[PlanStep]:
        return [s for s in self.nodes.values() if s.is_leaf]

    def get_depth(self) -> int:
        return max((s.level for s in self.nodes.values()), default=0)

    def get_all_steps(self) -> list[PlanStep]:
        return list(self.nodes.values())

    def get_steps_at_level(self, level: int) -> list[PlanStep]:
        return [s for s in self.nodes.values() if s.level == level]

    def flatten(self) -> list[PlanStep]:
        out = []
        def dfs(sid: str):
            out.append(self.nodes[sid])
            for cid in self.nodes[sid].child_step_ids:
                dfs(cid)
        dfs(self.root.step_id)
        return out

    def to_dict(self) -> dict:
        return {"root": asdict(self.root), "nodes": {k: asdict(v) for k, v in self.nodes.items()}}

    @classmethod
    def from_dict(cls, data: dict) -> "TaskTree":
        root = PlanStep(**data["root"])
        t = cls(root)
        t.nodes = {k: PlanStep(**v) for k, v in data["nodes"].items()}
        t.root = t.nodes[root.step_id]
        return t

    def print_tree(self) -> str:
        lines = [f"Goal: {self.root.name}"]
        def rec(sid: str, pref: str):
            children = self.nodes[sid].child_step_ids
            for i, cid in enumerate(children):
                branch = "└── " if i == len(children)-1 else "├── "
                lines.append(pref + branch + self.nodes[cid].name)
                rec(cid, pref + ("    " if i == len(children)-1 else "│   "))
        rec(self.root.step_id, "")
        return "\n".join(lines)

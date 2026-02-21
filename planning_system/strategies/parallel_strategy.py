from __future__ import annotations

from planning_system.graph.graph_builder import build_graph
from planning_system.models.plan import Plan

from .base_strategy import BaseStrategy


class ParallelStrategy(BaseStrategy):
    name = "parallel"
    description = "Parallel-first planning"

    def __init__(self, decomposition_engine):
        self.decomposition_engine = decomposition_engine

    def plan(self, goal, context):
        tree = self.decomposition_engine.decompose(goal, context)
        steps = tree.get_leaves()
        for s in steps:
            s.dependencies = []
        p = Plan(goal_id=goal.goal_id, title=goal.title, description=goal.description, steps=steps, root_step_ids=[s.step_id for s in steps], strategy_used=self.name)
        p.execution_graph = build_graph(tree)
        return p

    def is_suitable(self, goal, context):
        return 0.8 if "parallel" in goal.intent.qualifiers or goal.intent.action in {"train", "analyze"} else 0.4

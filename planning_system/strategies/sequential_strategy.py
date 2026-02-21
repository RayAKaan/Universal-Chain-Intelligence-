from __future__ import annotations

from planning_system.graph.graph_builder import build_graph
from planning_system.models.plan import Plan

from .base_strategy import BaseStrategy


class SequentialStrategy(BaseStrategy):
    name = "sequential"
    description = "Strict sequential planning"

    def __init__(self, decomposition_engine):
        self.decomposition_engine = decomposition_engine

    def plan(self, goal, context):
        tree = self.decomposition_engine.decompose(goal, context)
        steps = tree.get_leaves()
        for i in range(1, len(steps)):
            steps[i].dependencies = [steps[i-1].step_id]
        p = Plan(goal_id=goal.goal_id, title=goal.title, description=goal.description, steps=steps, root_step_ids=[steps[0].step_id] if steps else [], strategy_used=self.name)
        p.execution_graph = build_graph(tree)
        return p

    def is_suitable(self, goal, context):
        return 0.7 if len(goal.constraints) > 0 else 0.5

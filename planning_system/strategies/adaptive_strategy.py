from __future__ import annotations

from planning_system.graph.graph_builder import add_checkpoint_nodes, build_graph
from planning_system.models.plan import Plan

from .base_strategy import BaseStrategy


class AdaptiveStrategy(BaseStrategy):
    name = "adaptive"
    description = "Adaptive mixed planning"

    def __init__(self, decomposition_engine):
        self.decomposition_engine = decomposition_engine

    def plan(self, goal, context):
        tree = self.decomposition_engine.decompose(goal, context)
        steps = tree.get_leaves()
        for i, s in enumerate(steps):
            if i > 0 and i % 2 == 1:
                s.dependencies = [steps[i - 1].step_id]
        p = Plan(goal_id=goal.goal_id, title=goal.title, description=goal.description, steps=steps, root_step_ids=[s.step_id for s in steps if not s.dependencies], strategy_used=self.name)
        p.execution_graph = add_checkpoint_nodes(build_graph(tree), interval=5)
        return p

    def is_suitable(self, goal, context):
        return 0.9

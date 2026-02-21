from __future__ import annotations

from planning_system.decomposition.atomic_detector import is_atomic
from planning_system.decomposition.decomposition_strategies import (
    CapabilityDrivenDecomposition,
    HeuristicDecomposition,
    HybridDecomposition,
    RecursiveDecomposition,
    TemplateBasedDecomposition,
)
from planning_system.decomposition.task_tree import TaskTree
from planning_system.models.plan_step import PlanStep, StepType


class DecompositionError(Exception):
    pass


class DecompositionEngine:
    def __init__(self, capability_registry, strategy_engine, config):
        self.registry = capability_registry
        self.strategy_engine = strategy_engine
        self.config = config
        self._strategies = {
            "template": TemplateBasedDecomposition(),
            "heuristic": HeuristicDecomposition(),
            "capability": CapabilityDrivenDecomposition(capability_registry),
            "recursive": RecursiveDecomposition(capability_registry),
            "hybrid": HybridDecomposition(capability_registry),
        }
        self.current_strategy = "hybrid"

    def decompose(self, goal, context=None) -> TaskTree:
        root = PlanStep(name=goal.title, description=goal.description, step_type=StepType.COMPOSITE, is_leaf=False)
        tree = TaskTree(root)
        steps = self._strategies[self.current_strategy].decompose(goal, context)
        if not steps:
            raise DecompositionError("unable to decompose goal")
        prev = None
        for s in steps:
            tree.add_step(s, root.step_id)
            if prev:
                s.dependencies.append(prev.step_id)
                prev.dependents.append(s.step_id)
            prev = s
        return tree

    def decompose_step(self, step, context=None):
        return [PlanStep(name=f"{step.name}_subtask_{i+1}", description=step.description, level=step.level + 1) for i in range(2)]

    def is_atomic(self, step_description: str, context=None) -> bool:
        dummy = PlanStep(name=step_description.replace(" ", "_"), description=step_description)
        return is_atomic(dummy, self.registry)

    def set_strategy(self, strategy_name: str) -> None:
        if strategy_name in self._strategies:
            self.current_strategy = strategy_name

    def get_available_strategies(self) -> list[str]:
        return list(self._strategies.keys())

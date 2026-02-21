from __future__ import annotations

from planning_system.config import DECOMPOSITION_KNOWLEDGE, MAX_DECOMPOSITION_DEPTH
from planning_system.decomposition.atomic_detector import is_atomic
from planning_system.models.plan_step import PlanStep, StepType


class TemplateBasedDecomposition:
    name = "template"

    def decompose(self, goal, context=None):
        key = f"{goal.intent.action}_{goal.intent.target.split()[0]}".lower().replace(" ", "_")
        kb = DECOMPOSITION_KNOWLEDGE.get(key) or DECOMPOSITION_KNOWLEDGE.get(f"{goal.intent.action}_{goal.intent.domain}")
        if not kb:
            return []
        return [PlanStep(name=s, description=s.replace("_", " "), step_type=StepType.ATOMIC) for s in kb["steps"]]


class HeuristicDecomposition:
    name = "heuristic"
    KB = {
        "train": ["collect_data", "preprocess_data", "configure_model", "train", "evaluate", "save_model"],
        "deploy": ["build", "test", "push", "configure_infra", "deploy", "verify"],
        "analyze": ["load_data", "explore", "analyze", "report"],
        "build": ["design", "implement", "test", "deploy"],
        "process": ["load_data", "clean_data", "transform_data", "save_data"],
    }

    def decompose(self, goal, context=None):
        return [PlanStep(name=s, description=s.replace("_", " "), step_type=StepType.ATOMIC) for s in self.KB.get(goal.intent.action, ["execute_task"])]


class CapabilityDrivenDecomposition:
    name = "capability"

    def __init__(self, registry):
        self.registry = registry

    def decompose(self, goal, context=None):
        caps = self.registry.get_by_category(goal.intent.domain) or self.registry.get_all()[:5]
        return [PlanStep(name=c.name, description=c.description, step_type=StepType.ATOMIC) for c in caps[:8]]


class RecursiveDecomposition:
    name = "recursive"

    def __init__(self, registry):
        self.registry = registry

    def decompose(self, goal, context=None):
        base = HeuristicDecomposition().decompose(goal)
        out = []
        for step in base:
            out.append(step)
            if not is_atomic(step, self.registry):
                for sub in [f"{step.name}_part1", f"{step.name}_part2"]:
                    out.append(PlanStep(name=sub, description=sub.replace("_", " "), step_type=StepType.ATOMIC, level=1))
        return out[:MAX_DECOMPOSITION_DEPTH * 20]


class HybridDecomposition:
    name = "hybrid"

    def __init__(self, registry):
        self.template = TemplateBasedDecomposition()
        self.heuristic = HeuristicDecomposition()
        self.capability = CapabilityDrivenDecomposition(registry)

    def decompose(self, goal, context=None):
        steps = self.template.decompose(goal, context)
        if not steps:
            steps = self.heuristic.decompose(goal, context)
        if not steps:
            steps = self.capability.decompose(goal, context)
        names = {s.name for s in steps}
        for s in self.capability.decompose(goal, context):
            if s.name not in names and len(steps) < 12:
                steps.append(s)
        return steps

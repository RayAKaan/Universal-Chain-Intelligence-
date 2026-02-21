from __future__ import annotations

from datetime import datetime, timedelta, timezone

from planning_system.goals.goal_parser import (
    parse_action,
    parse_constraints,
    parse_domain,
    parse_inputs,
    parse_outputs,
    parse_qualifiers,
    parse_target,
)
from planning_system.goals.goal_schema import validate_goal_schema
from planning_system.models.goal import (
    Goal,
    GoalConstraint,
    GoalInput,
    GoalOutput,
    GoalStatus,
    GoalType,
    Intent,
    Priority,
)


class GoalInterpretationError(Exception):
    pass


class GoalInterpreter:
    def __init__(self, config: dict | None = None):
        self.config = config or {}

    def interpret(self, raw_input: str, context=None) -> Goal:
        action = parse_action(raw_input)
        target = parse_target(raw_input, action)
        domain = parse_domain(raw_input)
        qualifiers = parse_qualifiers(raw_input)
        constraints = [GoalConstraint(**c) for c in parse_constraints(raw_input)]
        goal_type = self._map_goal_type(action)
        goal = Goal(
            raw_input=raw_input,
            title=f"{action.title()} {target}"[:120],
            description=raw_input,
            goal_type=goal_type,
            priority=Priority.HIGH if "urgent" in raw_input.lower() else Priority.MEDIUM,
            intent=Intent(action=action, target=target, domain=domain, qualifiers=qualifiers),
            inputs=[GoalInput(**i) for i in parse_inputs(raw_input)],
            outputs=[GoalOutput(**o) for o in parse_outputs(raw_input)],
            constraints=constraints,
            status=GoalStatus.PLANNING,
            deadline=datetime.now(timezone.utc) + timedelta(hours=2),
        )
        issues = self.validate_goal(goal)
        if issues:
            raise GoalInterpretationError("; ".join(issues))
        return goal

    def interpret_structured(self, structured_input: dict) -> Goal:
        goal = Goal.from_dict(structured_input)
        issues = self.validate_goal(goal)
        if issues:
            raise GoalInterpretationError("; ".join(issues))
        return goal

    def refine(self, goal: Goal, additional_context: str) -> Goal:
        goal.description = f"{goal.description}\n{additional_context}".strip()
        goal.intent.qualifiers = sorted(set(goal.intent.qualifiers + parse_qualifiers(additional_context)))
        return goal

    def decompose_compound_goal(self, goal: Goal) -> list[Goal]:
        parts = [p.strip() for p in goal.raw_input.split(" and ") if p.strip()]
        if len(parts) <= 1:
            return [goal]
        out = []
        for p in parts:
            child = self.interpret(p)
            child.parent_goal_id = goal.goal_id
            out.append(child)
        goal.sub_goal_ids = [c.goal_id for c in out]
        return out

    def validate_goal(self, goal: Goal) -> list[str]:
        return validate_goal_schema(goal)

    def _map_goal_type(self, action: str) -> GoalType:
        mapping = {
            "build": GoalType.BUILD,
            "create": GoalType.BUILD,
            "transform": GoalType.TRANSFORM,
            "analyze": GoalType.ANALYZE,
            "deploy": GoalType.DEPLOY,
            "optimize": GoalType.OPTIMIZE,
            "fix": GoalType.FIX,
            "monitor": GoalType.MONITOR,
            "automate": GoalType.AUTOMATE,
            "query": GoalType.QUERY,
        }
        return mapping.get(action, GoalType.COMPOSITE)

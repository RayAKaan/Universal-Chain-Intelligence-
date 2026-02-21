from __future__ import annotations

from datetime import datetime, timezone

VALID_OPERATORS = {"lt", "gt", "eq", "lte", "gte", "between"}


def validate_goal_schema(goal) -> list[str]:
    issues = []
    if not goal.raw_input:
        issues.append("raw_input is required")
    if not goal.title:
        issues.append("title is required")
    if not goal.intent.action or not goal.intent.target:
        issues.append("intent.action and intent.target are required")
    for c in goal.constraints:
        if c.operator not in VALID_OPERATORS:
            issues.append(f"invalid constraint operator: {c.operator}")
    if goal.deadline and goal.deadline <= datetime.now(timezone.utc):
        issues.append("deadline must be in the future")
    return issues

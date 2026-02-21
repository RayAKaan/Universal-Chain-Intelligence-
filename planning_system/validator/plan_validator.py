from __future__ import annotations

from dataclasses import dataclass, field

from planning_system.validator.feasibility_checker import check_feasibility
from planning_system.validator.validation_rules import (
    AllStepsResolvableRule,
    CapabilityHealthRule,
    DependenciesExistRule,
    FallbacksExistRule,
    GraphAcyclicRule,
    InputsMappedRule,
    NoOrphanStepsRule,
    OutputsProducedRule,
    ResourceFeasibilityRule,
    RetryPoliciesRule,
    SingleEntryPointRule,
    TimeConstraintRule,
)


@dataclass
class ValidationReport:
    is_valid: bool
    score: float
    results: list = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    suggestions: list[str] = field(default_factory=list)


class PlanValidationError(Exception):
    pass


class PlanValidator:
    def __init__(self):
        self.rules = [
            GraphAcyclicRule(), AllStepsResolvableRule(), DependenciesExistRule(), InputsMappedRule(), OutputsProducedRule(),
            ResourceFeasibilityRule(), TimeConstraintRule(), CapabilityHealthRule(), SingleEntryPointRule(), NoOrphanStepsRule(),
            RetryPoliciesRule(), FallbacksExistRule(),
        ]

    def validate(self, plan, context=None) -> ValidationReport:
        results = [r.validate(plan, context) for r in self.rules]
        errors = [r.message for r in results if not r.passed and r.severity == "error"]
        warnings = [r.message for r in results if not r.passed and r.severity == "warning"]
        feas = check_feasibility(plan, context)
        score = max(0.0, 1.0 - (len(errors) * 0.2 + len(warnings) * 0.05)) * feas.feasibility_score
        return ValidationReport(not errors, score, results, errors, warnings, feas.suggestions)

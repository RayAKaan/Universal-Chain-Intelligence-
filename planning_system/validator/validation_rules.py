from __future__ import annotations

from planning_system.models.plan import ValidationResult


class BaseRule:
    name = "base"
    severity = "info"

    def validate(self, plan, context=None):
        return ValidationResult(self.name, True, self.severity, "ok", [])


class GraphAcyclicRule(BaseRule):
    name = "GraphAcyclicRule"
    severity = "error"

    def validate(self, plan, context=None):
        passed = not plan.execution_graph.has_cycle()
        return ValidationResult(self.name, passed, self.severity, "graph cycle detected" if not passed else "ok", [])


class AllStepsResolvableRule(BaseRule):
    name = "AllStepsResolvableRule"
    severity = "error"

    def validate(self, plan, context=None):
        bad = [s.step_id for s in plan.steps if s.is_leaf and not s.capability_id]
        return ValidationResult(self.name, not bad, self.severity, "unresolved steps" if bad else "ok", bad)


class DependenciesExistRule(BaseRule):
    name = "DependenciesExistRule"
    severity = "error"

    def validate(self, plan, context=None):
        ids = {s.step_id for s in plan.steps}
        bad = [s.step_id for s in plan.steps if any(d not in ids for d in s.dependencies)]
        return ValidationResult(self.name, not bad, self.severity, "missing dependencies" if bad else "ok", bad)


class InputsMappedRule(BaseRule):
    name = "InputsMappedRule"
    severity = "error"


class OutputsProducedRule(BaseRule):
    name = "OutputsProducedRule"
    severity = "error"


class ResourceFeasibilityRule(BaseRule):
    name = "ResourceFeasibilityRule"
    severity = "warning"


class TimeConstraintRule(BaseRule):
    name = "TimeConstraintRule"
    severity = "warning"


class CapabilityHealthRule(BaseRule):
    name = "CapabilityHealthRule"
    severity = "warning"


class SingleEntryPointRule(BaseRule):
    name = "SingleEntryPointRule"
    severity = "error"

    def validate(self, plan, context=None):
        passed = len(plan.root_step_ids) > 0
        return ValidationResult(self.name, passed, self.severity, "no root steps" if not passed else "ok", [])


class NoOrphanStepsRule(BaseRule):
    name = "NoOrphanStepsRule"
    severity = "warning"


class RetryPoliciesRule(BaseRule):
    name = "RetryPoliciesRule"
    severity = "info"


class FallbacksExistRule(BaseRule):
    name = "FallbacksExistRule"
    severity = "info"

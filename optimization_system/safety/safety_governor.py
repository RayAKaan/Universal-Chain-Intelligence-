from __future__ import annotations
from optimization_system.models.safety_report import SafetyReport, SafetyCheck
class SafetyGovernor:
    def __init__(self,impact_analyzer,guardrails,config): self.impact=impact_analyzer;self.guardrails=guardrails;self.config=config
    def check_guardrails(self,modification): return [v.message for v in self.guardrails.check_all(modification)]
    def evaluate_modification(self,modification):
        violations=self.guardrails.check_all(modification)
        safe=not any(v.blocking for v in violations)
        return SafetyReport(modification_id=modification.modification_id,is_safe=safe,risk_level='high' if violations else 'low',checks_performed=[SafetyCheck('guardrails',safe,'; '.join(v.message for v in violations),'high' if violations else 'low')],potential_impacts=[self.impact.analyze_impact(modification)],recommendation='reject' if violations else 'approve')
    def approve(self,modification): return self.evaluate_modification(modification).is_safe

from __future__ import annotations
from dataclasses import dataclass
from optimization_system.safety.safety_rules import get_all_rules, check_rule
@dataclass
class GuardrailViolation: guardrail_name:str; severity:str; message:str; blocking:bool=True
class Guardrails:
    def check_all(self,modification):
        out=[]
        for r in get_all_rules():
            ok,msg=check_rule(r['name'],modification)
            if not ok: out.append(GuardrailViolation(r['name'],'high',msg,True))
        return out

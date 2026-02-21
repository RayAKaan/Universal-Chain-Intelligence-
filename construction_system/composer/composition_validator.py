from __future__ import annotations
class CompositionError(Exception):pass
class CompositionValidator:
    def validate_composition(self,composition):
        issues=[]
        ids=set(composition.components)
        for w in composition.wirings:
            if w['source_component_id'] not in ids or w['target_component_id'] not in ids: issues.append('wiring references unknown component')
            if w['source_component_id']==w['target_component_id']: issues.append('self-cycle wiring')
        return issues

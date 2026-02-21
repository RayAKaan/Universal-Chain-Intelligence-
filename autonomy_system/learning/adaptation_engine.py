from __future__ import annotations
class AdaptationEngine:
    def adapt(self,system_state,learnings):
        return [{'change':'prefer_fast_processor','reason':'higher success'}] if learnings else []

from __future__ import annotations
from datetime import datetime, timezone
from autonomy_system.models.healing_event import HealingEvent, FailureType
class SelfHealer:
    def __init__(self,failure_detector,recovery_strategies,health_reconciler,circuit_breaker,watchdog,config):
        self.detector=failure_detector; self.recovery=recovery_strategies; self.reconciler=health_reconciler; self.breaker=circuit_breaker; self.watchdog=watchdog; self.config=config; self.history=[]; self.running=False
    def start(self): self.running=True; self.watchdog.start(self.config.WATCHDOG_INTERVAL_SECONDS)
    def stop(self): self.running=False; self.watchdog.stop()
    def heal(self,failure):
        ftype=FailureType(failure.get('failure_type','UNKNOWN')) if failure.get('failure_type') in FailureType.__members__.values() else FailureType.UNKNOWN
        ev=HealingEvent(failure_type=ftype,affected_phase=failure.get('phase','system'),affected_component=failure.get('component','unknown'),severity=failure.get('severity','medium'))
        strat=self.recovery.select(failure); ev.recovery_strategy=strat.__class__.__name__; ev.recovery_actions=['apply strategy']; ev.recovery_success=bool(strat.recover(failure)); ev.recovery_time=datetime.now(timezone.utc)
        self.history.append(ev); return ev
    def check_and_heal(self):
        events=[self.heal(f) for f in self.detector.detect_all()]
        self.reconciler.reconcile(); return events
    def get_healing_history(self): return self.history

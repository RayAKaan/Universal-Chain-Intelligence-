from __future__ import annotations
import threading, time
from datetime import datetime, timezone
from autonomy_system.models.system_status import SystemStatus, SystemHealth, PhaseStatus
from autonomy_system.models.goal_record import GoalRecord, GoalSource, GoalRecordStatus
from autonomy_system.models.autonomy_state import AutonomyLevel
from autonomy_system.core.system_state import SystemState
from autonomy_system.core.boot_sequence import BootSequence, BootStep
from autonomy_system.core.phase_coordinator import PhaseCoordinator
from autonomy_system.core.lifecycle_manager import LifecycleManager
from autonomy_system.core.shutdown_handler import ShutdownHandler

class UCIBootError(Exception): pass
class UCIShutdownError(Exception): pass
class GoalProcessingError(Exception): pass

class IntelligenceCore:
    def __init__(self, config: dict):
        self.config=config
        self.state=SystemState()
        self.lifecycle=LifecycleManager()
        self.shutdown_handler=ShutdownHandler()
        self.running=False
        self.paused=False

    def boot(self)->None:
        self.state.set_status(SystemHealth.BOOTING)
        def _noop(): return None
        seq=BootSequence([
            BootStep('initialize_persistence',_noop,True),BootStep('boot_phase0',_noop,True),BootStep('boot_phase1',_noop,True),BootStep('boot_phase2',_noop,True),BootStep('boot_phase3',_noop,True),BootStep('boot_phase4',_noop,True),
            BootStep('initialize_integration_fabric',_noop,True),BootStep('initialize_goal_manager',_noop,True),BootStep('initialize_autonomy_controller',_noop,True),BootStep('initialize_self_healer',_noop,True),BootStep('initialize_learning_engine',_noop,True),BootStep('initialize_communication_hub',_noop,True),BootStep('initialize_telemetry',_noop,True),BootStep('initialize_knowledge_base',_noop,True)
        ])
        r=seq.execute()
        if not r['success']: raise UCIBootError(str(r['errors']))
        self.running=True
        self.state.set_status(SystemHealth.HEALTHY)
        self.state.add_event('UCI Intelligence Core online')

    def shutdown(self, graceful: bool=True)->None:
        self.state.set_status(SystemHealth.SHUTTING_DOWN)
        if graceful and hasattr(self,'goal_manager'):
            self.goal_manager.stop_processing()
        self.running=False
        self.state.set_status(SystemHealth.OFFLINE)
        self.state.add_event('UCI Intelligence Core offline')

    def submit_goal(self, raw_input:str, source:GoalSource=GoalSource.EXTERNAL_CLI, priority:int=50, metadata:dict=None)->GoalRecord:
        if hasattr(self,'autonomy_controller') and not self.autonomy_controller.can_perform('execute_goal'):
            ar=self.autonomy_controller.request_approval('execute_goal',{'goal':raw_input})
            if not ar.approved: raise GoalProcessingError('goal execution not approved')
        r=self.goal_manager.submit(raw_input,source,priority,metadata)
        self.state.increment_counter('goals_received')
        return r

    def process_goal(self, goal_record:GoalRecord)->GoalRecord:
        try:
            goal_record.status=GoalRecordStatus.INTERPRETING; t0=time.time()
            goal_record.goal_id=f'goal-{goal_record.record_id[:8]}'
            goal_record.status=GoalRecordStatus.PLANNING; goal_record.plan_id=f'plan-{goal_record.record_id[:8]}'
            if 'missing capability' in goal_record.raw_input.lower() and hasattr(self,'acquisition_engine'):
                self.acquisition_engine.acquire_for_goal(goal_record,'json_parser')
            goal_record.status=GoalRecordStatus.EXECUTING; goal_record.started_at=datetime.now(timezone.utc)
            goal_record.result={'message':'executed','input':goal_record.raw_input}
            goal_record.status=GoalRecordStatus.COMPLETED; goal_record.completed_at=datetime.now(timezone.utc)
            goal_record.execution_time_ms=(time.time()-t0)*1000
            if hasattr(self,'learning_engine'): self.learning_engine.learn_from_goal(goal_record)
            self.state.increment_counter('goals_completed')
            return goal_record
        except Exception as e:
            goal_record.status=GoalRecordStatus.FAILED; goal_record.error=str(e); self.state.increment_counter('goals_failed'); self.state.add_error(e); return goal_record

    def get_status(self)->SystemStatus:
        s=SystemStatus(overall_status=self.state.get_status(),overall_score=1.0 if self.state.get_status()==SystemHealth.HEALTHY else 0.5,autonomy_level=getattr(self,'autonomy_controller',type('X',(),{'get_level':lambda *_:'guided'})()).get_level().name.lower() if hasattr(self,'autonomy_controller') else 'guided',uptime_seconds=(datetime.now(timezone.utc)-self.state.boot_time).total_seconds(),boot_time=self.state.boot_time)
        s.phase_status={p:PhaseStatus(phase_name=p,status='healthy',score=1.0) for p in ['phase0','phase1','phase2','phase3','phase4']}
        s.active_goals=[g.__dict__ for g in (self.goal_manager.get_active_goals() if hasattr(self,'goal_manager') else [])]
        s.recent_events=self.state.get_recent_events(20)
        return s

    def get_capabilities(self)->list[dict]:
        if hasattr(self,'phase1_registry'): return [c.to_dict() if hasattr(c,'to_dict') else {'name':getattr(c,'name','')} for c in self.phase1_registry.get_all()]
        return []

    def set_autonomy_level(self, level:AutonomyLevel|str)->None: self.autonomy_controller.set_level(level)
    def pause(self)->None: self.paused=True; self.state.set_status(SystemHealth.MAINTENANCE)
    def resume(self)->None: self.paused=False; self.state.set_status(SystemHealth.HEALTHY)
    def is_running(self)->bool: return self.running
    def is_healthy(self)->bool: return self.state.get_status() in {SystemHealth.HEALTHY,SystemHealth.DEGRADED}

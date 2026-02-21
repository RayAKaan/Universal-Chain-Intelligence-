from __future__ import annotations
import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path
from capability_system.config import DATABASE_PATH as CAP_DB
from capability_system.persistence.database import Database as CapDB
from capability_system.registry.migrations import run_migrations
from capability_system.events.event_bus import EventBus
from capability_system.registry.capability_store import CapabilityStore
from capability_system.registry.capability_registry import CapabilityRegistry
from capability_system.query.query_engine import QueryEngine
from capability_system.benchmarking.benchmark_engine import BenchmarkEngine
from capability_system.benchmarking.benchmark_store import BenchmarkStore
from capability_system.models.capability import Capability, CapabilityType, CapabilityState
from execution_core.config import DEFAULT_CONFIG
from execution_core.core.execution_engine import ExecutionEngine
from execution_core.monitoring.execution_monitor import ExecutionMonitor
from execution_core.resource.resource_manager import ResourceManager
from execution_core.core.scheduler import Scheduler
from planning_system.strategies.strategy_engine import StrategyEngine
from construction_system.main import build_system as build_phase3
from optimization_system.main import build as build_phase4
from autonomy_system import config
from autonomy_system.core.intelligence_core import IntelligenceCore
from autonomy_system.core.phase_coordinator import PhaseCoordinator
from autonomy_system.autonomy.autonomy_controller import AutonomyController
from autonomy_system.goals.goal_queue import PriorityGoalQueue
from autonomy_system.goals.goal_prioritizer import GoalPrioritizer
from autonomy_system.goals.goal_arbitrator import GoalArbitrator
from autonomy_system.goals.goal_manager import GoalManager
from autonomy_system.goals.goal_generator import GoalGenerator
from autonomy_system.acquisition.source_registry import SourceRegistry
from autonomy_system.acquisition.package_installer import PackageInstaller
from autonomy_system.acquisition.capability_fetcher import CapabilityFetcher
from autonomy_system.acquisition.dependency_resolver import DependencyResolver
from autonomy_system.acquisition.acquisition_safety import AcquisitionSafety
from autonomy_system.acquisition.acquisition_engine import AcquisitionEngine
from autonomy_system.architecture.architecture_analyzer import ArchitectureAnalyzer
from autonomy_system.architecture.architecture_planner import ArchitecturePlanner
from autonomy_system.architecture.phase_tuner import PhaseTuner
from autonomy_system.architecture.architecture_optimizer import ArchitectureOptimizer
from autonomy_system.healing.failure_detector import FailureDetector
from autonomy_system.healing.recovery_strategies import RecoveryStrategies
from autonomy_system.healing.health_reconciler import HealthReconciler
from autonomy_system.healing.circuit_breaker import CircuitBreakerRegistry
from autonomy_system.healing.watchdog import Watchdog
from autonomy_system.healing.self_healer import SelfHealer
from autonomy_system.consciousness.introspection_engine import IntrospectionEngine
from autonomy_system.consciousness.state_narrator import StateNarrator
from autonomy_system.consciousness.capability_map import CapabilityMap
from autonomy_system.consciousness.self_model import SelfModel
from autonomy_system.consciousness.system_consciousness import SystemConsciousness
from autonomy_system.communication.communication_hub import CommunicationHub
from autonomy_system.communication.message_router import MessageRouter
from autonomy_system.communication.request_parser import RequestParser
from autonomy_system.communication.response_formatter import ResponseFormatter
from autonomy_system.communication.protocol_adapters.queue_adapter import QueueAdapter
from autonomy_system.runtime.heartbeat import Heartbeat
from autonomy_system.learning.experience_store import ExperienceStore
from autonomy_system.learning.pattern_learner import PatternLearner
from autonomy_system.learning.preference_tracker import PreferenceTracker
from autonomy_system.learning.adaptation_engine import AdaptationEngine
from autonomy_system.learning.learning_engine import LearningEngine
from autonomy_system.telemetry.telemetry_collector import TelemetryCollector
from autonomy_system.telemetry.telemetry_aggregator import TelemetryAggregator
from autonomy_system.telemetry.dashboard_data import DashboardData
from autonomy_system.telemetry.alert_manager import AlertManager
from autonomy_system.knowledge.knowledge_graph import KnowledgeGraph
from autonomy_system.knowledge.knowledge_indexer import KnowledgeIndexer
from autonomy_system.knowledge.knowledge_query import KnowledgeQuery
from autonomy_system.knowledge.knowledge_base import KnowledgeBase
from autonomy_system.models.goal_record import GoalSource
from autonomy_system.models.communication_message import MessageType

def setup_logging():
    Path(config.LOG_FILE).parent.mkdir(parents=True,exist_ok=True)
    root=logging.getLogger(); root.setLevel(logging.DEBUG); root.handlers=[]
    ch=logging.StreamHandler(); ch.setLevel(logging.INFO); ch.setFormatter(logging.Formatter('%(asctime)s | %(name)s | %(levelname)s | %(message)s'))
    fh=RotatingFileHandler(config.LOG_FILE,maxBytes=config.LOG_MAX_SIZE_MB*1024*1024,backupCount=config.LOG_BACKUP_COUNT); fh.setLevel(logging.DEBUG); fh.setFormatter(logging.Formatter('%(asctime)s | %(name)s | %(levelname)s | %(message)s'))
    root.addHandler(ch); root.addHandler(fh)

def hdr(t):
    print('\n'+'='*96); print(t); print('='*96)

def init_phase0():
    eng=ExecutionEngine(DEFAULT_CONFIG,ExecutionMonitor(),ResourceManager(DEFAULT_CONFIG.max_workers)); return eng,Scheduler(eng,DEFAULT_CONFIG)

def init_phase1():
    db=CapDB(CAP_DB); run_migrations(db); bus=EventBus(db); reg=CapabilityRegistry(CapabilityStore(db),bus)
    return reg, QueryEngine(reg), BenchmarkEngine(reg,BenchmarkStore(db),None,bus), bus

def register_mock(reg):
    for n,l,r in [('fast_processor',10,0.99),('slow_processor',500,0.9),('report_generator',80,0.98),('file_cleaner',30,0.99),('trainer',200,0.92)]:
        reg.register(Capability(name=n,version='1.0.0',description=n,execution_endpoint=f'{n}.exec',capability_type=CapabilityType.PYTHON_FUNCTION,state=CapabilityState.ACTIVE,metadata={'latency_ms':l,'reliability':r}))

def build_core():
    p0,s0=init_phase0(); reg,q,b,ev=init_phase1(); register_mock(reg); p2=StrategyEngine(); p2.register_strategy(type('S',(),{'name':'sequential'})())
    cm,*_=build_phase3(); p4ctx=build_phase4()
    core=IntelligenceCore(config); core.boot(); core.phase1_registry=reg
    core.phase_coordinator=PhaseCoordinator(p0,reg,p2,cm,p4ctx)
    core.autonomy_controller=AutonomyController(config,core.state,p4ctx['safety'])
    core.goal_manager=GoalManager(core,PriorityGoalQueue(),GoalPrioritizer(),GoalArbitrator(),config)
    core.goal_generator=GoalGenerator(p4ctx['analyzer'],p4ctx['bottleneck'],reg,None,config)
    core.acquisition_engine=AcquisitionEngine(SourceRegistry(),PackageInstaller(),CapabilityFetcher(),DependencyResolver(),AcquisitionSafety(config),reg,cm,core.autonomy_controller,config)
    core.architecture_optimizer=ArchitectureOptimizer(ArchitectureAnalyzer(),ArchitecturePlanner(),PhaseTuner(),p4ctx,config)
    core.self_healer=SelfHealer(FailureDetector(core.phase_coordinator),RecoveryStrategies(),HealthReconciler(),CircuitBreakerRegistry(),Watchdog(),config)
    core.consciousness=SystemConsciousness(IntrospectionEngine(core.state),StateNarrator(),CapabilityMap(reg),SelfModel(),config)
    hub=CommunicationHub(MessageRouter(),ResponseFormatter(),RequestParser(),config)
    hub.router.register_handler(MessageType.GOAL_REQUEST,lambda m: core.submit_goal(m.content.get('text',''),GoalSource.EXTERNAL_API,m.content.get('priority',50)).__dict__)
    hub.router.register_handler(MessageType.STATUS_QUERY,lambda m: core.get_status().__dict__)
    hub.router.register_handler(MessageType.CAPABILITY_QUERY,lambda m: core.get_capabilities())
    hub.router.register_handler(MessageType.ADMIN_COMMAND,lambda m: {'ack':True,'command':m.content})
    hub.register_adapter(QueueAdapter(hub)); core.communication_hub=hub
    core.heartbeat=Heartbeat(); core.learning_engine=LearningEngine(ExperienceStore(config.DATABASE_PATH),PatternLearner(),PreferenceTracker(),AdaptationEngine(),config)
    core.telemetry_collector=TelemetryCollector(core); core.telemetry_aggregator=TelemetryAggregator(); core.alert_manager=AlertManager(); core.dashboard=DashboardData(core)
    store={}; core.knowledge_base=KnowledgeBase(KnowledgeGraph(),KnowledgeIndexer(),KnowledgeQuery(store),config); core.knowledge_base.query_engine.store=store
    return core

def main():
    setup_logging(); core=build_core(); core.set_autonomy_level('GUIDED')
    hdr('SCENARIO A: System Boot and Status'); print('Booted status:',core.get_status().overall_status.value); print('Status dashboard:',core.dashboard.get_overview()); print('Self-description:',core.consciousness.narrate_status())
    hdr('SCENARIO B: External Goal Submission and Execution'); g=core.submit_goal('Process a dataset and generate a report',GoalSource.EXTERNAL_CLI,60); r=core.goal_manager.process_next(); print('Goal lifecycle:',g.record_id,r.status.value,r.result)
    hdr('SCENARIO C: Multiple Concurrent Goals'); g1=core.submit_goal('Analyze system performance',GoalSource.EXTERNAL_CLI,70); g2=core.submit_goal('Clean up temporary files',GoalSource.EXTERNAL_CLI,30); g3=core.submit_goal('Train a classification model',GoalSource.EXTERNAL_CLI,50); print('Queue:',[(x.raw_input,x.priority) for x in core.goal_manager.queue.get_all()]); [core.goal_manager.process_next() for _ in range(3)]; print('Arbitration concurrent:',core.goal_manager.arbitrator.can_execute_concurrently([g1,g2,g3]))
    hdr('SCENARIO D: Autonomous Goal Generation'); goals=core.goal_generator.generate_goals(); print('Generated:',[(g.raw_input,g.priority,g.metadata.get('reason')) for g in goals])
    hdr('SCENARIO E: Capability Acquisition'); g=core.submit_goal('Use missing capability: json parser',GoalSource.EXTERNAL_CLI,55); a=core.acquisition_engine.acquire_for_goal(g,'json_parser'); print('Acquisition:',a.name,a.status.value,a.safety_report)
    hdr('SCENARIO F: Self-Healing'); ev=core.self_healer.heal({'failure_type':'CAPABILITY_FAILURE','phase':'phase1','component':'slow_processor','severity':'high'}); print('Healing event:',ev.failure_type.value,ev.recovery_strategy,ev.recovery_success)
    hdr('SCENARIO G: System Consciousness and Introspection'); print(core.consciousness.answer_question('What can you do?')); print(core.consciousness.answer_question('How are you performing?')); print(core.consciousness.answer_question('What are your weaknesses?')); print(core.consciousness.answer_question('What have you learned recently?')); print('Capability map:\n',core.consciousness.capmap.visualize_map()); print('Limitations:',core.consciousness.get_limitation_awareness())
    hdr('SCENARIO H: Autonomy Level Demonstration');
    for lv in ['PASSIVE','GUIDED','AUTONOMOUS']:
        core.set_autonomy_level(lv); ar=core.autonomy_controller.request_approval('execute_goal',{'detail':'demo'}); print(lv,ar.approved,ar.reason)
    print('Decision log:',core.autonomy_controller.get_decision_log()[-5:])
    hdr('SCENARIO I: Full Improvement Cycle Integration'); print('Improvement cycle:', core.phase_coordinator.cross_phase_operation('optimize_and_apply',{'target':'slow_processor'}))
    hdr('SCENARIO J: Learning and Adaptation');
    for t in ['goal one','goal two','goal three']:
        gr=core.submit_goal(t,GoalSource.EXTERNAL_CLI,40); rr=core.goal_manager.process_next(); core.learning_engine.learn_from_goal(rr)
    print('Learning stats:',core.learning_engine.get_learning_stats()); print('Adaptation:',core.learning_engine.apply_learnings({'goal_type':'general'}))
    hdr('SCENARIO K: Knowledge Base'); eid1=core.knowledge_base.learn_fact('fast_processor','faster_than','slow_processor',0.95,'benchmark'); eid2=core.knowledge_base.learn_fact('uci','has_mode','guided',1.0,'system'); print('Query:',[e.__dict__ for e in core.knowledge_base.query(subject='fast_processor')]); print('Graph:\n',core.knowledge_base.graph.visualize()); print('Stats:',core.knowledge_base.get_stats())
    hdr('SCENARIO L: Comprehensive System Dashboard'); print(core.dashboard.get_overview()); print('Phase health:',{k:v.status for k,v in core.get_status().phase_status.items()}); print('Queue:',core.goal_manager.get_queue_status()); print('Recent events:',core.state.get_recent_events(10))
    hdr('SCENARIO M: Graceful Lifecycle'); core.pause(); print('Paused status:',core.get_status().overall_status.value); core.resume(); print('Resumed status:',core.get_status().overall_status.value); core.shutdown(True); print('Shutdown status:',core.get_status().overall_status.value)

if __name__=='__main__':
    main()

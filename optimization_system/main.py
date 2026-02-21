from __future__ import annotations
import logging
from pathlib import Path
from capability_system.benchmarking.benchmark_engine import BenchmarkEngine
from capability_system.benchmarking.benchmark_store import BenchmarkStore
from capability_system.config import DATABASE_PATH as CAP_DB
from capability_system.events.event_bus import EventBus
from capability_system.persistence.database import Database as CapDB
from capability_system.query.query_engine import QueryEngine
from capability_system.registry.capability_registry import CapabilityRegistry
from capability_system.registry.capability_store import CapabilityStore
from capability_system.registry.migrations import run_migrations
from capability_system.models.capability import Capability, CapabilityState, CapabilityType
from execution_core.config import DEFAULT_CONFIG
from execution_core.core.execution_engine import ExecutionEngine
from execution_core.core.scheduler import Scheduler
from execution_core.monitoring.execution_monitor import ExecutionMonitor
from execution_core.resource.resource_manager import ResourceManager
from planning_system.strategies.strategy_engine import StrategyEngine
from construction_system.main import build_system as build_phase3
from optimization_system import config
from optimization_system.persistence.optimization_database import OptimizationDatabase
from optimization_system.performance.metric_store import MetricStore
from optimization_system.integration.phase0_optimizer_bridge import Phase0OptimizerBridge
from optimization_system.integration.phase1_optimizer_bridge import Phase1OptimizerBridge
from optimization_system.integration.phase2_optimizer_bridge import Phase2OptimizerBridge
from optimization_system.integration.phase3_optimizer_bridge import Phase3OptimizerBridge
from optimization_system.performance.performance_collector import PerformanceCollector
from optimization_system.performance.performance_aggregator import PerformanceAggregator
from optimization_system.performance.performance_analyzer import PerformanceAnalyzer
from optimization_system.bottleneck.bottleneck_detector import BottleneckDetector
from optimization_system.opportunity.opportunity_detector import OpportunityDetector
from optimization_system.opportunity.opportunity_ranker import OpportunityRanker
from optimization_system.knowledge.pattern_extractor import PatternExtractor
from optimization_system.knowledge.rule_engine import RuleEngine
from optimization_system.knowledge.knowledge_store import KnowledgeStore
from optimization_system.knowledge.knowledge_distiller import KnowledgeDistiller
from optimization_system.experiment.experiment_runner import ExperimentRunner
from optimization_system.experiment.experiment_analyzer import ExperimentAnalyzer
from optimization_system.experiment.experiment_store import ExperimentStore
from optimization_system.experiment.experiment_framework import ExperimentFramework
from optimization_system.regression.baseline_manager import BaselineManager
from optimization_system.regression.regression_detector import RegressionDetector
from optimization_system.safety.impact_analyzer import ImpactAnalyzer
from optimization_system.safety.guardrails import Guardrails
from optimization_system.safety.safety_governor import SafetyGovernor
from optimization_system.modification.modification_planner import ModificationPlanner
from optimization_system.modification.modification_applier import ModificationApplier
from optimization_system.modification.modification_validator import ModificationValidator
from optimization_system.modification.rollback_engine import RollbackEngine
from optimization_system.modification.self_modification_engine import SelfModificationEngine
from optimization_system.planner.optimization_planner import OptimizationPlanner
from optimization_system.planner.improvement_campaign import ImprovementCampaignManager
from optimization_system.capability.capability_ranker import CapabilityRanker
from optimization_system.capability.capability_pruner import CapabilityPruner
from optimization_system.capability.capability_evolver import CapabilityEvolver
from optimization_system.strategy.strategy_evaluator import StrategyEvaluator
from optimization_system.strategy.strategy_synthesizer import StrategySynthesizer
from optimization_system.strategy.strategy_optimizer import StrategyOptimizer
from optimization_system.resource.resource_analyzer import ResourceAnalyzer
from optimization_system.resource.resource_allocator import ResourceAllocator
from optimization_system.resource.resource_forecaster import ResourceForecaster
from optimization_system.resource.resource_optimizer import ResourceOptimizer
from optimization_system.tracker.improvement_history import ImprovementHistory
from optimization_system.tracker.improvement_tracker import ImprovementTracker
from optimization_system.tracker.improvement_metrics import ImprovementMetrics
from optimization_system.tracker.changelog import Changelog
from optimization_system.scheduler.cycle_manager import CycleResult

def hdr(t): print('\n'+'='*96+'\n'+t+'\n'+'='*96)

def setup_logging():
    Path(config.LOG_FILE).parent.mkdir(parents=True,exist_ok=True)
    logging.basicConfig(level=getattr(logging,config.LOG_LEVEL),format='%(asctime)s | %(name)s | %(levelname)s | %(message)s',handlers=[logging.StreamHandler(),logging.FileHandler(config.LOG_FILE)])

def init_phase0():
    eng=ExecutionEngine(DEFAULT_CONFIG,ExecutionMonitor(),ResourceManager(DEFAULT_CONFIG.max_workers))
    return eng,Scheduler(eng,DEFAULT_CONFIG)

def init_phase1():
    db=CapDB(CAP_DB);run_migrations(db);bus=EventBus(db);reg=CapabilityRegistry(CapabilityStore(db),bus)
    return reg,QueryEngine(reg),BenchmarkEngine(reg,BenchmarkStore(db),None,bus),bus

def register_mock_capabilities(reg):
    mocks=[('fast_processor',10,0.99,5),('slow_processor',500,0.95,1),('unreliable_api',50,0.70,4),('stable_api',80,0.99,3),('heavy_model',2000,0.98,2),('light_model',200,0.96,3),('legacy_tool',1000,0.80,0),('efficient_analyzer',30,0.99,6)]
    for n,l,r,u in mocks:
        reg.register(Capability(name=n,description=n,version='1.0.0',execution_endpoint=f'{n}.execute',capability_type=CapabilityType.PYTHON_FUNCTION,state=CapabilityState.ACTIVE,metadata={'latency_ms':l,'reliability':r,'usage':u,'days_since_used':60 if n=='legacy_tool' else 1}))

def build():
    p0_eng,p0_sched=init_phase0(); p1_reg,p1_query,p1_bench,p1_bus=init_phase1(); register_mock_capabilities(p1_reg)
    p2_strat=StrategyEngine(); p2_strat.register_strategy(type('S',(),{'name':'sequential'})()); p2_strat.register_strategy(type('S',(),{'name':'parallel'})())
    cm,re,cgen,validator,sandbox,composer,am,prov,_,_,_=build_phase3()
    db=OptimizationDatabase(config.DATABASE_PATH); ms=MetricStore(db)
    b0=Phase0OptimizerBridge(p0_eng,getattr(p0_eng, "_resource_manager", None),p0_sched)
    b1=Phase1OptimizerBridge(p1_reg,p1_query,p1_bench,None,p1_bus)
    b2=Phase2OptimizerBridge(None,p2_strat,None,None)
    b3=Phase3OptimizerBridge(cm,None,am)
    collector=PerformanceCollector(b0,b1,b2,b3,ms,config); aggregator=PerformanceAggregator(); analyzer=PerformanceAnalyzer(ms,b1,b2)
    bottleneck=BottleneckDetector(analyzer,ms,config)
    rule_engine=RuleEngine(); distiller=KnowledgeDistiller(PatternExtractor(),rule_engine,KnowledgeStore(db),config)
    opp_detector=OpportunityDetector(bottleneck,analyzer,distiller,p1_reg,config); opp_ranker=OpportunityRanker(config)
    exp_framework=ExperimentFramework(ExperimentRunner(b1,b2),ExperimentAnalyzer(),ExperimentStore(db),config)
    baseline=BaselineManager(ms,db); reg_detector=RegressionDetector(baseline,ms,config)
    safety=SafetyGovernor(ImpactAnalyzer(),Guardrails(),config)
    mod_planner=ModificationPlanner(); mod_engine=SelfModificationEngine(mod_planner,ModificationApplier(b0,b1,b2),ModificationValidator(),RollbackEngine(),safety,config)
    planner=OptimizationPlanner(opp_detector,b2,b3,safety,config); campaign_mgr=ImprovementCampaignManager()
    cap_rank=CapabilityRanker(b1,config); cap_pruner=CapabilityPruner(b1,config); cap_evolver=CapabilityEvolver(p1_reg,cap_rank,b3,exp_framework,config)
    strat_eval=StrategyEvaluator(b2); strat_opt=StrategyOptimizer(strat_eval,StrategySynthesizer(b3),b2,b3,config)
    res_opt=ResourceOptimizer(ResourceAnalyzer(),ResourceAllocator(),ResourceForecaster(ms),b0,config)
    history=ImprovementHistory(db); tracker=ImprovementTracker(db,history); tmetrics=ImprovementMetrics(tracker); clog=Changelog(history)
    return locals()

class SelfImprovementEngine:
    def __init__(self,ctx): self.__dict__.update(ctx)
    def should_experiment(self,op): return 'REPLACE' in op.opportunity_type.value
    def run_improvement_cycle(self):
        import time
        t=time.time();metrics=self.collector.collect_all();b=self.bottleneck.detect_all();ops=self.opp_detector.detect_all();selected=self.opp_ranker.rank(ops)[:config.TOP_N_IMPROVEMENTS_PER_CYCLE]
        applied=0;regressions=0
        for op in selected:
            campaign=self.planner.plan_improvement(op); self.campaign_mgr.execute_campaign(campaign)
            if self.should_experiment(op):
                e=self.exp_framework.run_experiment(self.exp_framework.create_capability_experiment('slow_processor','fast_processor',20))
                if e.conclusion!='treatment_wins': continue
            mod=self.mod_planner.plan_modification(op)
            if not self.safety.evaluate_modification(mod).is_safe: continue
            if not self.mod_engine.apply_modification(mod): continue
            regs=self.reg_detector.monitor_after_modification(mod)
            if regs: regressions+=len(regs); self.mod_engine.rollback(mod.modification_id); continue
            from optimization_system.models.improvement import Improvement, ImprovementType, ImprovementStatus
            imp=Improvement(title=op.title,description=op.description,opportunity_id=op.opportunity_id,campaign_id=campaign.campaign_id,improvement_type=ImprovementType.CUSTOM,target_phase=op.phase,target_component=op.component,status=ImprovementStatus.APPLIED,improvement_percent={'latency':op.estimated_improvement.get('improvement_percent',0)})
            self.tracker.record_improvement(imp); applied+=1
        self.distiller.distill();
        if applied: self.baseline.capture_baseline('post_cycle')
        return CycleResult(metrics_collected=len(metrics),bottlenecks_found=len(b),opportunities_found=len(ops),campaigns_planned=len(selected),improvements_applied=applied,regressions_detected=regressions,duration_ms=(time.time()-t)*1000)

def main():
    setup_logging();ctx=build();engine=SelfImprovementEngine(ctx)
    hdr('SCENARIO A: Performance Collection and Analysis');m=ctx['collector'].collect_all();print('Collected:',len(m));print('Health:',ctx['analyzer'].analyze_system_health());print('Phase metrics:',ctx['aggregator'].aggregate_by_phase(m));print('Performance score:',ctx['analyzer'].get_performance_score())
    hdr('SCENARIO B: Bottleneck Detection');bs=ctx['bottleneck'].detect_all();print('Bottlenecks:',[(b.bottleneck_type.value,b.component,b.severity.name) for b in bs]);
    if bs: print('Impact:',ctx['bottleneck'].analyzer.analyze_impact(bs[0])); print('Suggestions:',ctx['bottleneck'].analyzer.suggest_actions(bs[0]))
    hdr('SCENARIO C: Opportunity Detection and Ranking');ops=ctx['opp_detector'].detect_all();print('Top opportunities:',[(o.title,round(o.priority_score,3)) for o in ops[:5]])
    hdr('SCENARIO D: A/B Experiment');e=ctx['exp_framework'].run_experiment(ctx['exp_framework'].create_capability_experiment('slow_processor','fast_processor',30));print('Conclusion:',e.conclusion);print('P-values:',e.statistical_results.p_value);print('Confidence intervals:',e.statistical_results.confidence_interval);print('Effect size:',e.statistical_results.effect_size)
    hdr('SCENARIO E: Capability Evolution');print('Rankings:',ctx['cap_rank'].rank_all());print('Underperformers:',ctx['cap_rank'].identify_underperformers(0.5));print('Redundant:',ctx['cap_rank'].identify_redundant());print('Stale:',ctx['cap_pruner'].identify_candidates())
    hdr('SCENARIO F: Strategy Optimization');print('Strategy eval:',ctx['strat_eval'].evaluate_all());print('Recommendations:',ctx['strat_eval'].get_strategy_recommendations('general','default'));print('Comparison:',ctx['strat_eval'].compare_strategies('sequential','parallel'))
    hdr('SCENARIO G: Self-Modification with Safety');mod=ctx['mod_planner'].plan_capability_replacement('slow_processor','fast_processor');print('Safety report:',ctx['safety'].evaluate_modification(mod));print('Applied:',ctx['mod_engine'].apply_modification(mod));print('Regressions:',ctx['reg_detector'].monitor_after_modification(mod))
    hdr('SCENARIO H: Knowledge Distillation');rules=ctx['distiller'].distill();print('Rules:',[(r.name,r.condition.metric,r.action.action_type) for r in rules]);print('Triggered:',[(r.name,c) for r,c in ctx['rule_engine'].evaluate_rules({'latency_ms':500,'reliability':0.7,'system_cpu_usage_percent':95})])
    hdr('SCENARIO I: Full Improvement Cycle');print('Cycle result:',engine.run_improvement_cycle())
    hdr('SCENARIO J: Improvement History and Impact');print('Timeline:',ctx['tracker'].get_improvement_timeline());print('Impact:',ctx['tracker'].get_improvement_impact());print('Velocity:',ctx['tmetrics'].calculate_improvement_velocity());print('Success rate:',ctx['tmetrics'].calculate_success_rate());print('Changelog:\n',ctx['clog'].generate_summary())
    hdr('SCENARIO K: Baseline Comparison');b0=ctx['baseline'].capture_baseline('before');engine.run_improvement_cycle();b1=ctx['baseline'].capture_baseline('after');print('Comparison:',ctx['baseline'].compare_to_baseline(b0));print('After baseline:',b1.metrics)
    hdr('SCENARIO L: Resource Optimization');print('Utilization:',ctx['res_opt'].an.analyze_utilization());print('Waste:',ctx['res_opt'].an.analyze_waste());print('Reallocation:',ctx['res_opt'].al.propose_reallocation({'threads':8},{'threads':6}));print('Forecast:',ctx['res_opt'].fc.forecast_usage('system_cpu_usage_percent',6))

if __name__=='__main__': main()

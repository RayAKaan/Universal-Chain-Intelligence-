from __future__ import annotations

import logging
from pathlib import Path

from capability_system import config as phase1_config
from capability_system.benchmarking.benchmark_engine import BenchmarkEngine
from capability_system.benchmarking.benchmark_store import BenchmarkStore
from capability_system.events.event_bus import EventBus
from capability_system.integration.phase0_bridge import Phase0Bridge
from capability_system.models.capability import (
    Capability,
    CapabilityState,
    CapabilityType,
    ExecutionType,
    HealthStatus,
)
from capability_system.persistence.database import Database as CapabilityDB
from capability_system.query.query_engine import QueryEngine
from capability_system.registry.capability_registry import CapabilityRegistry
from capability_system.registry.capability_store import CapabilityStore
from capability_system.registry.migrations import run_migrations
from execution_core.config import DEFAULT_CONFIG
from execution_core.core.execution_engine import APITaskHandler, ExecutionEngine, ExternalScriptHandler, PythonFunctionHandler, ShellCommandHandler
from execution_core.core.scheduler import Scheduler
from execution_core.monitoring.execution_monitor import ExecutionMonitor
from execution_core.resource.resource_manager import ResourceManager
from planning_system import config
from planning_system.constraints.constraint_engine import ConstraintEngine
from planning_system.context.context_manager import ContextManager
from planning_system.context.execution_history import ExecutionHistory
from planning_system.context.planning_memory import PlanningMemory
from planning_system.decomposition.decomposition_engine import DecompositionEngine
from planning_system.feedback.feedback_engine import FeedbackEngine
from planning_system.feedback.strategy_learner import StrategyLearner
from planning_system.goals.goal_interpreter import GoalInterpreter
from planning_system.graph.graph_analyzer import calculate_critical_path, estimate_total_duration
from planning_system.graph.graph_visualizer import visualize_status, visualize_text, visualize_timeline
from planning_system.integration.phase0_adapter import Phase0Adapter
from planning_system.integration.phase1_adapter import Phase1Adapter
from planning_system.integration.unified_bridge import UnifiedBridge
from planning_system.models.constraint import Constraint, ConstraintType
from planning_system.models.goal import GoalType
from planning_system.monitor.failure_handler import FailureHandler
from planning_system.monitor.plan_monitor import PlanMonitor
from planning_system.optimizer.plan_optimizer import PlanOptimizer
from planning_system.resolver.capability_resolver import CapabilityResolver
from planning_system.store.plan_store import PlanStore
from planning_system.store.plan_versioning import PlanVersioning
from planning_system.strategies.adaptive_strategy import AdaptiveStrategy
from planning_system.strategies.parallel_strategy import ParallelStrategy
from planning_system.strategies.sequential_strategy import SequentialStrategy
from planning_system.strategies.strategy_engine import StrategyEngine
from planning_system.validator.plan_validator import PlanValidationError, PlanValidator
from planning_system.executor.rollback_manager import RollbackManager
from planning_system.executor.step_executor import StepExecutor
from planning_system.executor.plan_executor import PlanExecutor


class PlanningEngine:
    def __init__(self, components):
        self.goal_interpreter = components["goal_interpreter"]
        self.context_manager = components["context_manager"]
        self.strategy_engine = components["strategy_engine"]
        self.capability_resolver = components["capability_resolver"]
        self.plan_optimizer = components["plan_optimizer"]
        self.plan_validator = components["plan_validator"]
        self.plan_store = components["plan_store"]
        self.plan_executor = components["plan_executor"]
        self.feedback_engine = components["feedback_engine"]

    def execute_goal(self, raw_input: str):
        goal = self.goal_interpreter.interpret(raw_input)
        context = self.context_manager.create_context(goal)
        strategy = self.strategy_engine.select_strategy(goal, context)
        plan = strategy.plan(goal, context)
        plan = self.capability_resolver.resolve_plan(plan)
        plan = self.plan_optimizer.optimize(plan)
        report = self.plan_validator.validate(plan, context)
        if not report.is_valid:
            raise PlanValidationError(report)
        self.plan_store.save_goal(goal)
        self.plan_store.save(plan)
        result = self.plan_executor.execute(plan, context)
        self.feedback_engine.record_outcome(goal, plan, result)
        self.plan_store.save_execution_result(result)
        return goal, plan, result


def setup_logging():
    Path(config.LOG_FILE).parent.mkdir(parents=True, exist_ok=True)
    logging.basicConfig(level=getattr(logging, config.LOG_LEVEL), format="%(asctime)s | %(name)s | %(levelname)s | %(message)s", handlers=[logging.StreamHandler(), logging.FileHandler(config.LOG_FILE)])
    logging.getLogger("execution_core").setLevel(logging.WARNING)


def header(title):
    print("\n" + "=" * 88)
    print(title)
    print("=" * 88)


def init_phase0():
    monitor = ExecutionMonitor()
    rm = ResourceManager(DEFAULT_CONFIG.max_workers)
    engine = ExecutionEngine(DEFAULT_CONFIG, monitor, rm)
    engine.register_handler("PythonFunctionTask", PythonFunctionHandler())
    engine.register_handler("ShellCommandTask", ShellCommandHandler())
    engine.register_handler("ExternalScriptTask", ExternalScriptHandler())
    engine.register_handler("APITask", APITaskHandler())
    scheduler = Scheduler(engine, DEFAULT_CONFIG)
    return engine, scheduler, rm


def init_phase1():
    db = CapabilityDB(phase1_config.DATABASE_PATH)
    run_migrations(db)
    bus = EventBus(db)
    reg = CapabilityRegistry(CapabilityStore(db), bus)
    q = QueryEngine(reg)
    bridge = Phase0Bridge(reg)
    bengine = BenchmarkEngine(reg, BenchmarkStore(db), bridge, bus)
    return reg, q, bengine


def register_mock_capabilities(registry):
    defs = [
        ("data_loader", "data", "load data", CapabilityType.PYTHON_FUNCTION, ExecutionType.PYTHON_FUNCTION),
        ("data_preprocessor", "data", "clean transform data", CapabilityType.PYTHON_FUNCTION, ExecutionType.PYTHON_FUNCTION),
        ("model_trainer", "ml", "train model", CapabilityType.PYTHON_FUNCTION, ExecutionType.PYTHON_FUNCTION),
        ("model_evaluator", "ml", "evaluate model", CapabilityType.PYTHON_FUNCTION, ExecutionType.PYTHON_FUNCTION),
        ("model_saver", "ml", "save model", CapabilityType.PYTHON_FUNCTION, ExecutionType.PYTHON_FUNCTION),
        ("report_generator", "data", "generate report", CapabilityType.PYTHON_FUNCTION, ExecutionType.PYTHON_FUNCTION),
        ("shell_executor", "system", "execute shell command", CapabilityType.SHELL_COMMAND, ExecutionType.SHELL_COMMAND),
        ("file_writer", "system", "write files", CapabilityType.PYTHON_FUNCTION, ExecutionType.PYTHON_FUNCTION),
        ("http_requester", "api", "http request", CapabilityType.REST_API, ExecutionType.API_CALL),
        ("json_processor", "data", "process json", CapabilityType.PYTHON_FUNCTION, ExecutionType.PYTHON_FUNCTION),
    ]
    for name, category, desc, ctype, etype in defs:
        cap = Capability(name=name, version="1.0.0", capability_type=ctype, category=category, subcategory="generic", description=desc, execution_endpoint="builtins.print" if etype == ExecutionType.PYTHON_FUNCTION else ("echo" if etype == ExecutionType.SHELL_COMMAND else "https://httpbin.org/get"), execution_type=etype, execution_config={}, state=CapabilityState.REGISTERED, health_status=HealthStatus.HEALTHY)
        cid = registry.register(cap)
        registry.activate(cid)


def build_components():
    p0_engine, p0_scheduler, p0_rm = init_phase0()
    p1_registry, p1_query, p1_benchmark = init_phase1()
    register_mock_capabilities(p1_registry)

    phase0_adapter = Phase0Adapter(p0_engine, p0_scheduler, p0_rm)
    phase1_adapter = Phase1Adapter(p1_registry, p1_query, p1_benchmark)
    unified = UnifiedBridge(phase0_adapter, phase1_adapter)

    store = PlanStore(config.DATABASE_PATH)
    planning_memory = PlanningMemory(store)
    strategy_learner = StrategyLearner()

    goal_interpreter = GoalInterpreter()
    strategy_engine = StrategyEngine()
    decomposition_engine = DecompositionEngine(p1_registry, strategy_engine, config)
    strategy_engine.register_strategy(SequentialStrategy(decomposition_engine))
    strategy_engine.register_strategy(ParallelStrategy(decomposition_engine))
    strategy_engine.register_strategy(AdaptiveStrategy(decomposition_engine))

    resolver = CapabilityResolver(p1_registry, p1_query, config)
    optimizer = PlanOptimizer(None, None, config)
    validator = PlanValidator()
    monitor = PlanMonitor(EventBus(), config)
    rollback = RollbackManager()
    failure_handler = FailureHandler()
    context_manager = ContextManager(phase1_adapter)
    step_executor = StepExecutor(unified, context_manager)
    executor = PlanExecutor(phase0_adapter, phase1_adapter, monitor, rollback, config, step_executor, failure_handler)
    feedback = FeedbackEngine(planning_memory, strategy_learner)
    constraint_engine = ConstraintEngine()
    versioning = PlanVersioning(store)
    history = ExecutionHistory()

    return {
        "goal_interpreter": goal_interpreter,
        "context_manager": context_manager,
        "strategy_engine": strategy_engine,
        "decomposition_engine": decomposition_engine,
        "capability_resolver": resolver,
        "plan_optimizer": optimizer,
        "plan_validator": validator,
        "plan_executor": executor,
        "plan_monitor": monitor,
        "constraint_engine": constraint_engine,
        "plan_store": store,
        "feedback_engine": feedback,
        "versioning": versioning,
        "history": history,
    }


def run_scenarios(engine: PlanningEngine, components):
    header("SCENARIO A: Simple Sequential Goal")
    goal, plan, result = engine.execute_goal("Process a CSV data file")
    print("Goal:", goal.intent)
    print("Plan steps:", [s.name for s in plan.steps])
    print(visualize_text(plan.execution_graph))
    print("Validation score:", components["plan_validator"].validate(plan, components["context_manager"].create_context(goal)).score)
    print("Execution status:", result.status, "completed:", result.steps_completed)

    header("SCENARIO B: Complex Parallel Goal")
    goal2, plan2, result2 = engine.execute_goal("Train an image classification model")
    print("Intent:", goal2.intent)
    print("Graph levels:", [[n.step.name for n in lvl] for lvl in plan2.execution_graph.get_execution_levels()])
    print("Critical path:", calculate_critical_path(plan2.execution_graph))
    before = estimate_total_duration(plan2.execution_graph, parallel=False)
    after = estimate_total_duration(plan2.execution_graph, parallel=True)
    print(f"Optimization before/after ms: {before:.1f} -> {after:.1f}")
    print(visualize_timeline(plan2.execution_graph))

    header("SCENARIO C: Goal with Constraints")
    goal3, plan3, _ = engine.execute_goal("Deploy a web service within 5 minutes using minimal resources")
    constraints = [Constraint(constraint_type=ConstraintType.TIME, name="max_duration", parameter="duration", operator="lte", value=300000, unit="ms", is_hard=True)]
    report = components["constraint_engine"].evaluate(plan3, constraints)
    print("Extracted constraints:", [c.__dict__ for c in goal3.constraints])
    print("Constraint report all_satisfied:", report.all_satisfied)

    header("SCENARIO D: Failure and Recovery")
    for s in plan3.steps:
        if "deploy" in s.name:
            s.execution_type = "shell_command"
            s.input_mapping = {"command": {"source": "literal", "value": "false"}}
            s.on_failure = s.on_failure.RETRY
    ctx = components["context_manager"].create_context(goal3)
    ctx.plan_id = plan3.plan_id
    res_fail = components["plan_executor"].execute(plan3, ctx)
    print("Failure scenario status:", res_fail.status, "failed:", res_fail.steps_failed)

    header("SCENARIO E: Strategy Comparison")
    gtext = "Analyze dataset and generate report"
    goal_e = components["goal_interpreter"].interpret(gtext)
    ctx_e = components["context_manager"].create_context(goal_e)
    for name in components["strategy_engine"].list_strategies():
        strategy = components["strategy_engine"].get_strategy(name)
        p = strategy.plan(goal_e, ctx_e)
        p = components["capability_resolver"].resolve_plan(p)
        p = components["plan_optimizer"].optimize(p)
        print(name, "duration", p.total_estimated_duration_ms, "parallelism", p.execution_graph.get_parallelism_degree())

    header("SCENARIO F: Feedback and Learning")
    for txt in ["Process data", "Train model", "Analyze data"]:
        g, p, r = engine.execute_goal(txt)
        components["history"].record_execution(p.plan_id, r)
    rec = components["feedback_engine"].get_recommendations(goal2)
    print("Recommendations:", rec)

    header("SCENARIO G: Plan Versioning")
    g, p, _ = engine.execute_goal("Create report from JSON")
    v1 = {"version": p.version, "steps": [s.name for s in p.steps], "strategy_used": p.strategy_used}
    p.version += 1
    p.steps.append(p.steps[-1].__class__(name="export_report", description="export report"))
    components["plan_store"].save(p)
    v2 = {"version": p.version, "steps": [s.name for s in p.steps], "strategy_used": p.strategy_used}
    diff = components["versioning"].diff(v1, v2)
    print("Version history:", [v1["version"], v2["version"]])
    print("Diff:", diff)


def main():
    setup_logging()
    components = build_components()
    engine = PlanningEngine(components)
    run_scenarios(engine, components)


if __name__ == "__main__":
    main()

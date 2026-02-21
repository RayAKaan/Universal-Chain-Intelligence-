from __future__ import annotations

import json
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
from execution_core.config import DEFAULT_CONFIG
from execution_core.core.execution_engine import APITaskHandler, ExecutionEngine, ExternalScriptHandler, PythonFunctionHandler, ShellCommandHandler
from execution_core.core.scheduler import Scheduler
from execution_core.monitoring.execution_monitor import ExecutionMonitor
from execution_core.resource.resource_manager import ResourceManager
from planning_system.strategies.strategy_engine import StrategyEngine

from construction_system import config
from construction_system.artifacts.artifact_manager import ArtifactManager
from construction_system.artifacts.artifact_store import ArtifactStore
from construction_system.composer.component_composer import ComponentComposer
from construction_system.composer.composition_validator import CompositionValidator
from construction_system.composer.interface_matcher import InterfaceMatcher
from construction_system.composer.wiring_engine import WiringEngine
from construction_system.construction.capability_constructor import CapabilityConstructor
from construction_system.construction.construction_manager import ConstructionManager
from construction_system.construction.pipeline_constructor import PipelineConstructor
from construction_system.construction.service_constructor import ServiceConstructor
from construction_system.construction.strategy_constructor import StrategyConstructor
from construction_system.construction.system_constructor import SystemConstructor
from construction_system.construction.tool_constructor import ToolConstructor
from construction_system.codegen.code_formatter import CodeFormatter
from construction_system.codegen.code_generator import CodeGenerator
from construction_system.codegen.code_synthesizer import CodeSynthesizer
from construction_system.integration.construction_capability_handler import register_construction_capabilities
from construction_system.integration.phase1_constructor_bridge import Phase1ConstructorBridge
from construction_system.integration.phase2_constructor_bridge import Phase2ConstructorBridge
from construction_system.models.component import Component, ComponentType
from construction_system.models.composition import Composition
from construction_system.models.recursive_task import RecursiveTask
from construction_system.models.specification import SpecType, Specification
from construction_system.persistence.construction_database import ConstructionDatabase
from construction_system.provenance.provenance_store import ProvenanceStore
from construction_system.provenance.provenance_tracker import ProvenanceTracker
from construction_system.recursive.recursion_controller import RecursionController
from construction_system.recursive.recursive_engine import RecursiveExecutionEngine
from construction_system.recursive.subtask_generator import SubtaskGenerator
from construction_system.sandbox.sandbox_manager import SandboxManager
from construction_system.specifications.spec_language import SpecBuilder
from construction_system.specifications.spec_resolver import SpecResolver
from construction_system.specifications.spec_validator import SpecValidator
from construction_system.templates.template_library import TemplateLibrary
from construction_system.templates.template_registry import TemplateRegistry
from construction_system.validation.code_validator import CodeValidator
from construction_system.validation.static_analyzer import StaticAnalyzer
from construction_system.validation.syntax_checker import SyntaxChecker
from construction_system.validation.test_runner import TestRunner


def hdr(s: str) -> None:
    print("\n" + "=" * 96)
    print(s)
    print("=" * 96)


def setup_logging() -> None:
    Path(config.LOG_FILE).parent.mkdir(parents=True, exist_ok=True)
    logging.basicConfig(level=getattr(logging, config.LOG_LEVEL), format="%(asctime)s | %(name)s | %(levelname)s | %(message)s", handlers=[logging.StreamHandler(), logging.FileHandler(config.LOG_FILE)])


def init_phase0():
    eng = ExecutionEngine(DEFAULT_CONFIG, ExecutionMonitor(), ResourceManager(DEFAULT_CONFIG.max_workers))
    eng.register_handler("PythonFunctionTask", PythonFunctionHandler())
    eng.register_handler("ShellCommandTask", ShellCommandHandler())
    eng.register_handler("ExternalScriptTask", ExternalScriptHandler())
    eng.register_handler("APITask", APITaskHandler())
    return eng, Scheduler(eng, DEFAULT_CONFIG)


def init_phase1():
    db = CapDB(CAP_DB)
    run_migrations(db)
    bus = EventBus(db)
    reg = CapabilityRegistry(CapabilityStore(db), bus)
    return reg, QueryEngine(reg), BenchmarkEngine(reg, BenchmarkStore(db), None, bus), bus


def init_phase2():
    return StrategyEngine(), None


def build_system():
    p0_engine, p0_sched = init_phase0()
    p1_reg, p1_query, p1_bench, p1_bus = init_phase1()
    p2_strat, p2_plan = init_phase2()

    cdb = ConstructionDatabase(config.DATABASE_PATH)
    tlib = TemplateLibrary(TemplateRegistry(), config)
    cgen = CodeGenerator(tlib, CodeSynthesizer(), CodeFormatter(), config)
    validator = CodeValidator(SyntaxChecker(), StaticAnalyzer(), TestRunner(config), config)
    sandbox = SandboxManager(config)
    prov = ProvenanceTracker(ProvenanceStore(cdb))
    am = ArtifactManager(ArtifactStore(cdb), prov, config)
    composer = ComponentComposer(InterfaceMatcher(), WiringEngine(), CompositionValidator(), config)

    sys_ctor = SystemConstructor(cgen, validator, sandbox, am, composer, config)
    pipe_ctor = PipelineConstructor(cgen, validator, sandbox, am, composer, config)
    cap_ctor = CapabilityConstructor(cgen, validator, sandbox, am, composer, config)
    strat_ctor = StrategyConstructor(cgen, validator, sandbox, am, composer, config)
    tool_ctor = ToolConstructor(cgen, validator, sandbox, am, composer, config)
    svc_ctor = ServiceConstructor(cgen, validator, sandbox, am, composer, config)

    phase1_bridge = Phase1ConstructorBridge(p1_reg, None, p1_bus)
    phase2_bridge = Phase2ConstructorBridge(p2_strat, p2_plan)
    rc = RecursionController(config)
    subgen = SubtaskGenerator()

    cm = ConstructionManager(SpecValidator(), SpecResolver(), tlib, [cap_ctor, strat_ctor, pipe_ctor, tool_ctor, svc_ctor, sys_ctor], subgen, None, validator, sandbox, am, prov, phase1_bridge, phase2_bridge, cdb, config, capability_registry=p1_reg)
    re = RecursiveExecutionEngine(None, cm, rc, None, config)
    cm.recursive_engine = re

    cap_ids = register_construction_capabilities(phase1_bridge)
    return cm, re, cgen, validator, sandbox, composer, am, prov, p1_reg, p2_strat, cap_ids


def scenario_a(cgen, validator, sandbox):
    hdr("SCENARIO A: Generate a Python Function")
    spec = SpecBuilder.function("calculate_statistics").with_parameter("numbers", "list[float]", True).returns("dict").with_body(["import statistics", "return {'mean': statistics.mean(numbers), 'median': statistics.median(numbers), 'std_dev': statistics.pstdev(numbers) if len(numbers)>1 else 0.0}"]).with_docstring("Calculate mean/median/std_dev.").build()
    unit = cgen.generate_function({"name": spec.name, "parameters": [{"name": "numbers", "type": "list[float]"}], "return_type": "dict", "body_logic": spec.metadata["body_lines"], "docstring": spec.description})
    report = validator.validate([unit], None)
    sb = sandbox.execute_in_sandbox(unit.code + "\nprint(calculate_statistics([1,2,3]))\n")
    print("Specification:", spec.to_dict())
    print("Generated code:\n", unit.code)
    print("Validation valid:", report.is_valid)
    print("Sandbox output:", sb.stdout.strip())


def scenario_b(cgen, validator, sandbox):
    hdr("SCENARIO B: Generate a Python Class")
    spec = SpecBuilder.class_("DataProcessor").with_init([{"name": "config", "type": "dict"}]).with_method("load", [{"name": "path"}], "dict", ["return {}"]).with_method("process", [], "dict", ["return {}"]).with_method("save", [{"name": "path"}], "bool", ["return True"]).with_method("get_stats", [], "dict", ["return {'rows':0}"]).with_docstring("Data processor class").build()
    unit = cgen.generate_class({"name": spec.name, "methods": [{"action": "load"}, {"action": "process"}, {"action": "save"}, {"action": "get_stats"}], "docstring": spec.description})
    tests = cgen.generate_tests([unit])[0]
    rep = validator.validate([unit, tests], None)
    tr = TestRunner(config).run_tests(tests.code.replace("from target import "+unit.name, ""), unit.code)
    print("Generated class:\n", unit.code)
    print("Generated test:\n", tests.code)
    print("Validation:", rep.is_valid, "Tests:", tr)


def scenario_c(cm):
    hdr("SCENARIO C: Build a Data Pipeline")
    spec = SpecBuilder.pipeline("four_stage_pipeline").with_stage("LoadStage", "path", "data", "read").with_stage("CleanStage", "data", "data", "clean").with_stage("TransformStage", "data", "data", "transform").with_stage("SaveStage", "data", "path", "save").build()
    res = cm.construct(spec)
    print("Directory structure:", res.blueprint.directory_structure)
    print("Generated files:", res.files_created)
    print("Validation:", res.validation_results)


def scenario_d(cm, p1_reg):
    hdr("SCENARIO D: Construct a New Capability")
    spec = SpecBuilder.capability("text_word_counter").with_input_schema({"text": "str"}).with_output_schema({"counts": "dict"}).with_processing(["words = payload.get('text','').split()", "return {'counts': {w: words.count(w) for w in set(words)}}"]).with_category("nlp", "word_count").build()
    res = cm.construct(spec)
    constructed = [c for c in p1_reg.get_all() if c.name == "text_word_counter"]
    print("Plugin files:", [f for f in res.files_created if "plugin" in f or "manifest" in f])
    print("Registered capability:", constructed[0].capability_id if constructed else "not found")


def scenario_e(cm, p2_strat):
    hdr("SCENARIO E: Construct a New Planning Strategy")
    spec = SpecBuilder.strategy("priority_first_strategy").with_description("Execute highest-priority steps first").with_planning_logic(["return None"]).with_suitability({"default": 0.8}).build()
    res = cm.construct(spec)
    print("Generated strategy files:", [f for f in res.files_created if "strategy" in f])
    print("Strategies now:", p2_strat.list_strategies())


def scenario_f(cm, sandbox):
    hdr("SCENARIO F: Build a CLI Tool")
    spec = SpecBuilder.tool("file_analyzer").with_config({"commands": ["count", "stats", "search"]}).build()
    res = cm.construct(spec)
    code = "\n".join([Path(f).read_text() for f in res.files_created if f.endswith('.py')][:1])
    sb = sandbox.execute_in_sandbox(code + "\nprint('cli-ok')\n") if code else None
    print("Generated files:", res.files_created)
    print("Sandbox:", sb.stdout.strip() if sb else "no run")


def scenario_g(composer):
    hdr("SCENARIO G: Compose Multiple Components")
    c1 = Component(name="DataProcessor", component_type=ComponentType.LIBRARY)
    c2 = Component(name="Pipeline", component_type=ComponentType.COMPOSITE)
    comp = composer.auto_compose([c1, c2])
    res = composer.compose([c1, c2], comp)
    print("Composition plan:", comp.__dict__)
    print("Integration code:", res.code_units[0].code if res.code_units else "")
    print("Validation errors:", res.errors)


def scenario_h(re):
    hdr("SCENARIO H: Recursive Construction")
    sys_spec = SpecBuilder.system("mini_etl_system").with_component("data_reader", Specification(name="data_reader", spec_type=SpecType.MODULE)).with_component("data_transformer", Specification(name="data_transformer", spec_type=SpecType.MODULE)).with_component("data_writer", Specification(name="data_writer", spec_type=SpecType.MODULE)).with_component("orchestrator", Specification(name="orchestrator", spec_type=SpecType.MODULE)).build()
    t = RecursiveTask(name=sys_spec.name, description=sys_spec.description, specification=sys_spec, root_task_id="", max_depth=4)
    t.root_task_id = t.task_id
    res = re.execute_recursive(t)
    print("Task tree:", re.get_execution_tree(t.root_task_id))
    print("Generated files:", res.files_created)


def scenario_i(am, prov):
    hdr("SCENARIO I: Full Provenance Tracking")
    all_artifacts = am.get_all_artifacts()
    if not all_artifacts:
        print("No artifacts to track")
        return
    a = all_artifacts[0]
    chain = prov.get_provenance(a.artifact_id)
    print("Provenance chain length:", len(chain))
    print("Lineage:", prov.get_lineage(a.artifact_id))


def scenario_j(p1_reg, p2_strat, am, cap_ids):
    hdr("SCENARIO J: Self-Registration Verification")
    constructed_caps = [c for c in p1_reg.get_all() if c.metadata.get("source") == "constructed"]
    print("New capabilities registered in Phase 1:", [c.name for c in constructed_caps])
    print("New strategies in Phase 2:", p2_strat.list_strategies())
    print("Total artifacts created:", am.get_stats())
    if constructed_caps:
        print("Executable capability check (name):", constructed_caps[0].name)
    print("Construction capability IDs:", cap_ids)


def main() -> None:
    setup_logging()
    cm, re, cgen, validator, sandbox, composer, am, prov, p1_reg, p2_strat, cap_ids = build_system()
    scenario_a(cgen, validator, sandbox)
    scenario_b(cgen, validator, sandbox)
    scenario_c(cm)
    scenario_d(cm, p1_reg)
    scenario_e(cm, p2_strat)
    scenario_f(cm, sandbox)
    scenario_g(composer)
    scenario_h(re)
    scenario_i(am, prov)
    scenario_j(p1_reg, p2_strat, am, cap_ids)


if __name__ == "__main__":
    main()

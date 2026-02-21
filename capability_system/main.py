from __future__ import annotations

import logging
import os
from collections import Counter
from pathlib import Path

from capability_system import config
from capability_system.benchmarking.benchmark_engine import BenchmarkEngine
from capability_system.benchmarking.benchmark_store import BenchmarkStore
from capability_system.discovery.discovery_engine import DiscoveryEngine
from capability_system.discovery.scanners.api_scanner import APIScanner
from capability_system.discovery.scanners.local_scanner import LocalScanner
from capability_system.discovery.scanners.model_scanner import ModelScanner
from capability_system.discovery.scanners.network_scanner import NetworkScanner
from capability_system.discovery.scanners.plugin_scanner import PluginScanner
from capability_system.discovery.scanners.python_env_scanner import PythonEnvScanner
from capability_system.discovery.scanners.system_binary_scanner import SystemBinaryScanner
from capability_system.events.event_bus import EventBus
from capability_system.integration.phase0_bridge import Phase0Bridge
from capability_system.lifecycle.lifecycle_manager import LifecycleManager
from capability_system.health.health_monitor import HealthMonitor
from capability_system.models.capability import Capability, CapabilityState, CapabilityType, ExecutionType, HealthStatus
from capability_system.persistence.database import Database
from capability_system.query.query_engine import QueryEngine
from capability_system.registry.capability_registry import CapabilityRegistry
from capability_system.registry.capability_store import CapabilityStore
from capability_system.registry.migrations import run_migrations


def setup_logging() -> None:
    Path(config.LOG_FILE).parent.mkdir(parents=True, exist_ok=True)
    logging.getLogger("execution_core").setLevel(logging.WARNING)
    logging.basicConfig(
        level=getattr(logging, config.LOG_LEVEL, logging.INFO),
        format="%(asctime)s | %(name)s | %(levelname)s | %(message)s",
        handlers=[logging.StreamHandler(), logging.FileHandler(config.LOG_FILE)],
    )


def demo_add_function(x: int, y: int) -> int:
    return x + y


def print_header(title: str) -> None:
    print("\n" + "=" * 80)
    print(title)
    print("=" * 80)


def main() -> None:
    setup_logging()
    Path("data").mkdir(exist_ok=True)
    db = Database(config.DATABASE_PATH)
    run_migrations(db)

    event_bus = EventBus(db)
    registry = CapabilityRegistry(CapabilityStore(db), event_bus)

    discovery_engine = DiscoveryEngine(registry, event_bus, config)
    for scanner in [
        LocalScanner(),
        PythonEnvScanner(),
        SystemBinaryScanner(),
        APIScanner(),
        NetworkScanner(),
        ModelScanner(),
        PluginScanner(),
    ]:
        discovery_engine.register_scanner(scanner)

    bridge = Phase0Bridge(registry)
    benchmark_engine = BenchmarkEngine(registry, BenchmarkStore(db), bridge, event_bus)
    lifecycle_manager = LifecycleManager(registry, db, event_bus)
    health_monitor = HealthMonitor(
        registry,
        lifecycle_manager,
        event_bus,
        degraded_threshold=config.HEALTH_CONSECUTIVE_FAILURES_DEGRADED,
        failed_threshold=config.HEALTH_CONSECUTIVE_FAILURES_FAILED,
    )
    query_engine = QueryEngine(registry)

    print_header("A. Full Discovery Scan")
    discovery_results = discovery_engine.run_full_scan()
    discovered_count = sum(len(r.capabilities_found) for r in discovery_results)
    print(f"Discovered {discovered_count} capabilities")
    type_counts = Counter(c.capability_type.value for c in registry.get_all())
    cat_counts = Counter(c.category for c in registry.get_all())
    print("By type:", dict(type_counts))
    print("By category:", dict(cat_counts))

    print_header("B. Register 3 Manual Capabilities")
    py_cap = Capability(
        name="manual_add_function",
        version="1.0.0",
        capability_type=CapabilityType.PYTHON_FUNCTION,
        category="data",
        subcategory="math",
        description="Simple math addition",
        execution_endpoint="capability_system.main.demo_add_function",
        execution_type=ExecutionType.PYTHON_FUNCTION,
        execution_config={"args": [5, 7]},
        state=CapabilityState.REGISTERED,
        metadata={"source": "manual", "author": "uci", "license": "MIT", "tags": ["math", "python"], "documentation_url": "", "repository_url": ""},
    )
    shell_cap = Capability(
        name="manual_echo",
        version="1.0.0",
        capability_type=CapabilityType.SHELL_COMMAND,
        category="system",
        subcategory="shell",
        description="Echo command",
        execution_endpoint="echo",
        execution_type=ExecutionType.SHELL_COMMAND,
        execution_config={"command": "echo hello-from-capability"},
        state=CapabilityState.REGISTERED,
        metadata={"source": "manual", "author": "uci", "license": "MIT", "tags": ["shell"], "documentation_url": "", "repository_url": ""},
    )
    api_cap = Capability(
        name="httpbin_get",
        version="1.0.0",
        capability_type=CapabilityType.REST_API,
        category="network",
        subcategory="http",
        description="HTTPBin get endpoint",
        execution_endpoint="https://httpbin.org/get",
        execution_type=ExecutionType.API_CALL,
        execution_config={"url": "https://httpbin.org/get", "method": "GET"},
        state=CapabilityState.REGISTERED,
        metadata={"source": "manual", "author": "uci", "license": "MIT", "tags": ["api"], "documentation_url": "", "repository_url": ""},
    )
    ids = [registry.register(c) for c in [py_cap, shell_cap, api_cap]]
    for cid in ids:
        registry.activate(cid)
    print("Registered capability IDs:", ids)

    print_header("C. Benchmark 2 Capabilities")
    for cid in ids[:2]:
        from capability_system.benchmarking.benchmark_suite import BenchmarkSuite, TestCase
        suite = BenchmarkSuite(suite_id="demo_suite", name="Demo Suite", test_cases=[TestCase(input_data={"args":[1,2],"kwargs":{}})], iterations=20, warmup_iterations=2, timeout_ms=5000)
        result = benchmark_engine.benchmark(cid, suite=suite)
        print(f"{cid}: avg={result.avg_latency_ms:.3f}ms p95={result.p95_latency_ms:.3f}ms reliability={result.reliability:.2f}")

    print_header("D. Query Capabilities")
    network_caps = query_engine.filter({"category": "network"})
    print("Search by category=network:", [c.name for c in network_caps][:10])
    python_caps = query_engine.filter({"type": CapabilityType.PYTHON_FUNCTION})
    print("Filter by type=PYTHON_FUNCTION:", [c.name for c in python_caps][:10])
    ranked = query_engine.rank(registry.get_all(), "reliability")
    print("Top by reliability:", [c.name for c in ranked[:5]])

    print_header("E. Health Check Active Capabilities")
    summary = Counter(health_monitor.check_all().values())
    print("Health summary:", {k.value: v for k, v in summary.items()})

    print_header("F. Last 20 Events")
    for evt in event_bus.get_event_history(limit=20):
        print(f"{evt.timestamp.isoformat()} | {evt.event_type.value} | {evt.source} | {evt.data}")

    print_header("G. Registry Statistics")
    print("Total capabilities:", registry.count())
    print("By state:", {k.value: v for k, v in registry.count_by_state().items()})
    print("By type:", dict(Counter(c.capability_type.value for c in registry.get_all())))
    print("By health:", dict(Counter(c.health_status.value for c in registry.get_all())))

    print_header("H. Phase 0 Integration")
    exec_result = bridge.execute_capability(ids[0], {"function": demo_add_function, "args": [9, 3]})
    print("Bridge execution result:", exec_result)


if __name__ == "__main__":
    main()

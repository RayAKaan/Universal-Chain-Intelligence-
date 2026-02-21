from __future__ import annotations

import logging
import threading
import time
from datetime import datetime, timezone

from capability_system.benchmarking.benchmark_runner import BenchmarkRunner
from capability_system.benchmarking.benchmark_suite import BenchmarkSuite, api_call_suite, model_inference_suite, python_function_suite, shell_command_suite
from capability_system.events.event_types import Event, EventType
from capability_system.models.capability import CapabilityType, PerformanceProfile


class BenchmarkEngine:
    def __init__(self, registry, benchmark_store, phase0_bridge, event_bus):
        self.logger = logging.getLogger("capability_system.benchmark.engine")
        self.registry = registry
        self.store = benchmark_store
        self.runner = BenchmarkRunner(phase0_bridge)
        self.event_bus = event_bus
        self._thread = None
        self._stop = threading.Event()

    def _suite_for_capability(self, capability) -> BenchmarkSuite:
        if capability.capability_type.name in {"PYTHON_FUNCTION", "PYTHON_CLASS"}:
            return python_function_suite()
        if capability.capability_type.name in {"SHELL_COMMAND", "SYSTEM_BINARY", "EXTERNAL_SCRIPT"}:
            return shell_command_suite()
        if capability.capability_type.name == "REST_API":
            return api_call_suite()
        return model_inference_suite()

    def benchmark(self, capability_id: str, suite: BenchmarkSuite | None = None):
        cap = self.registry.get(capability_id)
        suite = suite or self._suite_for_capability(cap)
        self.event_bus.publish(Event(EventType.BENCHMARK_STARTED, "benchmark_engine", {"capability_id": capability_id}))
        result = self.runner.run(cap, suite)
        self.store.save(result)
        profile = cap.performance_profile
        profile.avg_latency_ms = result.avg_latency_ms
        profile.p50_latency_ms = result.p50_latency_ms
        profile.p95_latency_ms = result.p95_latency_ms
        profile.p99_latency_ms = result.p99_latency_ms
        profile.throughput_per_second = result.throughput_per_second
        profile.reliability = result.reliability
        profile.last_benchmark_at = datetime.now(timezone.utc)
        profile.benchmark_count += 1
        self.registry.update_performance_profile(capability_id, profile)
        self.event_bus.publish(Event(EventType.CAPABILITY_BENCHMARKED, "benchmark_engine", {"capability_id": capability_id, "result_id": result.result_id}))
        self.event_bus.publish(Event(EventType.BENCHMARK_COMPLETED, "benchmark_engine", {"capability_id": capability_id}))
        return result

    def benchmark_all(self, filter: dict | None = None):
        caps = self.registry.get_all()
        if filter:
            for k, v in filter.items():
                caps = [c for c in caps if getattr(c, k) == v]
        return [self.benchmark(c.capability_id) for c in caps if c.is_enabled]

    def schedule_benchmarks(self, interval_hours: int = 24) -> None:
        if self._thread and self._thread.is_alive():
            return

        def loop():
            while not self._stop.is_set():
                try:
                    self.benchmark_all()
                except Exception:
                    self.logger.exception("Scheduled benchmark failure")
                time.sleep(interval_hours * 3600)

        self._stop.clear()
        self._thread = threading.Thread(target=loop, daemon=True)
        self._thread.start()

    def get_results(self, capability_id: str):
        return self.store.load_by_capability(capability_id)

    def compare(self, capability_ids: list[str]) -> dict:
        out = {}
        for cid in capability_ids:
            latest = self.store.load_latest(cid)
            out[cid] = {
                "avg_latency_ms": latest.avg_latency_ms if latest else None,
                "reliability": latest.reliability if latest else None,
                "throughput": latest.throughput_per_second if latest else None,
            }
        return out

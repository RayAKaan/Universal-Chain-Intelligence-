from __future__ import annotations

import os
import platform
import statistics
import time

from capability_system.benchmarking.benchmark_metrics import calculate_latency_stats, calculate_reliability, calculate_throughput
from capability_system.models.benchmark_result import BenchmarkResult

try:
    import psutil
except Exception:  # noqa: BLE001
    psutil = None


class BenchmarkRunner:
    def __init__(self, phase0_bridge):
        self.phase0_bridge = phase0_bridge

    def run(self, capability, suite) -> BenchmarkResult:
        samples, success, failure, errors = [], 0, 0, 0
        peak_cpu, peak_mem = 0.0, 0.0

        for _ in range(suite.warmup_iterations):
            try:
                self.phase0_bridge.execute_capability(capability.capability_id, suite.test_cases[0].input_data)
            except Exception:
                pass

        start_all = time.perf_counter()
        for _ in range(suite.iterations):
            t0 = time.perf_counter()
            try:
                self.phase0_bridge.execute_capability(capability.capability_id, suite.test_cases[0].input_data)
                success += 1
            except TimeoutError:
                errors += 1
            except Exception:
                failure += 1
            samples.append((time.perf_counter() - t0) * 1000)
            if psutil:
                peak_cpu = max(peak_cpu, psutil.cpu_percent(interval=0.0))
                peak_mem = max(peak_mem, psutil.virtual_memory().used / (1024 * 1024))

        duration = time.perf_counter() - start_all
        stats = calculate_latency_stats(samples)
        reliability = calculate_reliability(success, suite.iterations)
        throughput = calculate_throughput(samples, duration)
        return BenchmarkResult(
            capability_id=capability.capability_id,
            benchmark_suite_id=suite.suite_id,
            latency_samples=samples,
            avg_latency_ms=stats["avg"],
            p50_latency_ms=stats["p50"],
            p95_latency_ms=stats["p95"],
            p99_latency_ms=stats["p99"],
            min_latency_ms=stats["min"],
            max_latency_ms=stats["max"],
            std_dev_latency_ms=stats["std_dev"],
            throughput_per_second=throughput,
            success_count=success,
            failure_count=failure,
            error_count=errors,
            timeout_count=0,
            reliability=reliability,
            resource_usage={"peak_cpu_percent": peak_cpu, "peak_memory_mb": peak_mem, "peak_gpu_percent": 0.0, "peak_gpu_memory_mb": 0.0},
            environment={"python_version": platform.python_version(), "os": platform.platform(), "cpu_model": platform.processor(), "total_memory_mb": int(psutil.virtual_memory().total/(1024*1024)) if psutil else 0, "gpu_model": ""},
            is_valid=True,
        )

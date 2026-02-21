from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Callable


@dataclass
class TestCase:
    input_data: Any
    expected_output: Any | None = None
    validation_function: Callable[[Any, Any], bool] | None = None


@dataclass
class BenchmarkSuite:
    suite_id: str
    name: str
    test_cases: list[TestCase] = field(default_factory=list)
    iterations: int = 100
    timeout_ms: int = 30000
    warmup_iterations: int = 10


def python_function_suite() -> BenchmarkSuite:
    return BenchmarkSuite(suite_id="python_function_suite", name="Python Function Suite", test_cases=[TestCase(input_data={"args": [1, 2], "kwargs": {}})])


def shell_command_suite() -> BenchmarkSuite:
    return BenchmarkSuite(suite_id="shell_command_suite", name="Shell Command Suite", test_cases=[TestCase(input_data={})], iterations=20, warmup_iterations=2)


def api_call_suite() -> BenchmarkSuite:
    return BenchmarkSuite(suite_id="api_call_suite", name="API Call Suite", test_cases=[TestCase(input_data={})], iterations=20, warmup_iterations=2)


def model_inference_suite() -> BenchmarkSuite:
    return BenchmarkSuite(suite_id="model_inference_suite", name="Model Inference Suite", test_cases=[TestCase(input_data={})], iterations=20, warmup_iterations=2)

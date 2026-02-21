from __future__ import annotations

import time

from construction_system.sandbox.sandbox_manager import SandboxManager


class TestRunner:
    def __init__(self, config=None):
        self.sandbox = SandboxManager(config)

    def run_tests(self, test_code, target_code, sandbox=True):
        start = time.time()
        combined = target_code + "\n\n" + test_code + "\n\nif __name__=='__main__':\n import unittest;unittest.main(exit=False)\n"
        r = self.sandbox.execute_in_sandbox(combined)
        ok = r.execution_success and "FAILED" not in r.stdout
        return {
            "total": 1,
            "passed": 1 if ok else 0,
            "failed": 0 if ok else 1,
            "errors": 0,
            "skipped": 0,
            "duration_ms": (time.time() - start) * 1000,
            "details": [{"test_name": "generated", "status": "passed" if ok else "failed", "message": r.stderr or r.stdout, "duration_ms": (time.time() - start) * 1000}],
        }

    def run_test_file(self, test_file_path):
        code = open(test_file_path).read()
        return self.run_tests(code, "")

    def run_test_suite(self, test_files):
        out = {"total": 0, "passed": 0, "failed": 0, "errors": 0, "skipped": 0, "duration_ms": 0.0, "details": []}
        for f in test_files:
            r = self.run_test_file(f)
            for k in ("total", "passed", "failed", "errors", "skipped", "duration_ms"):
                out[k] += r[k]
            out["details"] += r["details"]
        return out

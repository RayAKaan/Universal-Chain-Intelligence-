from __future__ import annotations

import importlib.metadata as md
import logging
import time

from capability_system import config
from capability_system.discovery.scanners.base_scanner import BaseScanner
from capability_system.models.capability import Capability, CapabilityState, CapabilityType, ExecutionType
from capability_system.models.discovery_result import DiscoveryResult


class PythonEnvScanner(BaseScanner):
    scanner_name = "python_env_scanner"
    scanner_type = "python_env"

    def __init__(self) -> None:
        self.logger = logging.getLogger("capability_system.discovery.python_env")

    def is_available(self) -> bool:
        return True

    def scan(self) -> DiscoveryResult:
        start = time.perf_counter()
        caps, errors = [], []
        def _to_semver(v: str) -> str:
            parts=[]
            for token in v.replace("-", ".").split("."):
                digits="".join(ch for ch in token if ch.isdigit())
                if digits:
                    parts.append(str(int(digits)))
            while len(parts) < 3:
                parts.append("0")
            return ".".join(parts[:3])

        max_packages = 120
        for idx, dist in enumerate(md.distributions()):
            if idx >= max_packages:
                break
            try:
                name = dist.metadata.get("Name", "")
                if not name or name in config.EXCLUDED_PYTHON_PACKAGES:
                    continue
                caps.append(
                    Capability(
                        name=name,
                        version=_to_semver(dist.version or "0.0.0"),
                        capability_type=CapabilityType.PYTHON_CLASS,
                        category="python",
                        subcategory="package",
                        description=f"Python package {name}",
                        execution_endpoint=name,
                        execution_type=ExecutionType.PYTHON_FUNCTION,
                        metadata={"source": "python_env_scan", "author": "", "license": "", "tags": ["python"], "documentation_url": "", "repository_url": ""},
                        state=CapabilityState.DISCOVERED,
                    )
                )
            except Exception as exc:
                errors.append(str(exc))
        return DiscoveryResult(scanner_name=self.scanner_name, source_type="python_env", source_location="local", capabilities_found=caps, scan_duration_ms=(time.perf_counter()-start)*1000, errors=errors)

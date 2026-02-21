from __future__ import annotations

import logging
import time

from capability_system.discovery.scanners.base_scanner import BaseScanner
from capability_system.discovery.scanners.model_scanner import ModelScanner
from capability_system.discovery.scanners.plugin_scanner import PluginScanner
from capability_system.discovery.scanners.python_env_scanner import PythonEnvScanner
from capability_system.discovery.scanners.system_binary_scanner import SystemBinaryScanner
from capability_system.models.discovery_result import DiscoveryResult


class LocalScanner(BaseScanner):
    scanner_name = "local_scanner"
    scanner_type = "local"

    def __init__(self):
        self.logger = logging.getLogger("capability_system.discovery.local")
        self.scanners = [PythonEnvScanner(), SystemBinaryScanner(), ModelScanner(), PluginScanner()]

    def is_available(self) -> bool:
        return True

    def scan(self) -> DiscoveryResult:
        start = time.perf_counter()
        caps, errors = [], []
        for scanner in self.scanners:
            try:
                if scanner.is_available():
                    result = scanner.scan()
                    caps.extend(result.capabilities_found)
                    errors.extend(result.errors)
            except Exception as exc:
                errors.append(f"{scanner.scanner_name}: {exc}")
        return DiscoveryResult(scanner_name=self.scanner_name, source_type="local", source_location="host", capabilities_found=caps, scan_duration_ms=(time.perf_counter()-start)*1000, errors=errors)

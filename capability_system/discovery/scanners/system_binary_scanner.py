from __future__ import annotations

import logging
import os
import subprocess
import time

from capability_system import config
from capability_system.discovery.scanners.base_scanner import BaseScanner
from capability_system.models.capability import Capability, CapabilityState, CapabilityType, ExecutionType
from capability_system.models.discovery_result import DiscoveryResult


class SystemBinaryScanner(BaseScanner):
    scanner_name = "system_binary_scanner"
    scanner_type = "system_binary"

    def __init__(self):
        self.logger = logging.getLogger("capability_system.discovery.system_binary")

    def is_available(self) -> bool:
        return True

    def scan(self) -> DiscoveryResult:
        start = time.perf_counter()
        caps, errors, seen = [], [], set()
        max_binaries = 250
        for path_dir in os.getenv("PATH", "").split(os.pathsep):
            if not os.path.isdir(path_dir):
                continue
            try:
                for entry in os.listdir(path_dir):
                    if len(seen) >= max_binaries:
                        break
                    full = os.path.join(path_dir, entry)
                    if entry in seen or not os.path.isfile(full) or not os.access(full, os.X_OK):
                        continue
                    seen.add(entry)
                    meta = config.KNOWN_TOOLS.get(entry, {"category": "system", "subcategory": "unknown"})
                    version = "0.0.0"
                    if entry in config.KNOWN_TOOLS:
                        try:
                            out = subprocess.run([full, "--version"], capture_output=True, text=True, timeout=0.2, check=False)
                            version = (out.stdout or out.stderr).splitlines()[0][:20] or "0.0.0"
                        except Exception:
                            pass
                    caps.append(Capability(name=entry, version="1.0.0", capability_type=CapabilityType.SYSTEM_BINARY, category=meta["category"], subcategory=meta["subcategory"], description=f"System binary: {entry} ({version})", execution_endpoint=full, execution_type=ExecutionType.SHELL_COMMAND, metadata={"source":"local_scan","author":"","license":"","tags":["binary"],"documentation_url":"","repository_url":""}, state=CapabilityState.DISCOVERED))
            except Exception as exc:
                errors.append(str(exc))
        return DiscoveryResult(scanner_name=self.scanner_name, source_type="system", source_location="PATH", capabilities_found=caps, scan_duration_ms=(time.perf_counter()-start)*1000, errors=errors)

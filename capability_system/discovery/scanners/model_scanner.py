from __future__ import annotations

import logging
import os
import subprocess
import time
from pathlib import Path

from capability_system import config
from capability_system.discovery.scanners.base_scanner import BaseScanner
from capability_system.models.capability import Capability, CapabilityState, CapabilityType, ExecutionType, ResourceRequirements
from capability_system.models.discovery_result import DiscoveryResult

MODEL_EXTS = {".pt", ".onnx", ".bin", ".safetensors", ".gguf"}


class ModelScanner(BaseScanner):
    scanner_name = "model_scanner"
    scanner_type = "model"

    def __init__(self):
        self.logger = logging.getLogger("capability_system.discovery.model")

    def is_available(self) -> bool:
        return True

    def scan(self) -> DiscoveryResult:
        start = time.perf_counter()
        caps, errors = [], []
        max_files = 200
        seen = 0
        for directory in config.MODEL_DIRECTORIES:
            base = Path(directory).expanduser()
            if not base.exists():
                continue
            base_depth = len(base.parts)
            for root, _, files in os.walk(base):
                if len(Path(root).parts) - base_depth > 2:
                    continue
                for file in files:
                    if seen >= max_files:
                        break
                    p = Path(root) / file
                    if p.suffix.lower() in MODEL_EXTS:
                        size_mb = int(p.stat().st_size / (1024 * 1024))
                        caps.append(Capability(name=p.stem, version="1.0.0", capability_type=CapabilityType.MODEL_INFERENCE, category="ml", subcategory="model_file", description=f"Model file {p.name}", execution_endpoint=str(p), execution_type=ExecutionType.MODEL_INFERENCE, resource_requirements=ResourceRequirements(min_memory_mb=max(256, size_mb)), metadata={"source":"local_scan","author":"","license":"","tags":["model"],"documentation_url":"","repository_url":""}, state=CapabilityState.DISCOVERED))
                    seen += 1
                if seen >= max_files:
                    break
        try:
            out = subprocess.run(["ollama", "list"], capture_output=True, text=True, timeout=2, check=False)
            if out.returncode == 0:
                for line in out.stdout.splitlines()[1:]:
                    name = line.split()[0]
                    if name:
                        caps.append(Capability(name=name, version="1.0.0", capability_type=CapabilityType.MODEL_INFERENCE, category="ml", subcategory="ollama", description="Ollama model", execution_endpoint=name, execution_type=ExecutionType.MODEL_INFERENCE, metadata={"source":"local_scan","author":"","license":"","tags":["ollama"],"documentation_url":"","repository_url":""}, state=CapabilityState.DISCOVERED))
        except Exception:
            pass
        return DiscoveryResult(scanner_name=self.scanner_name, source_type="model", source_location="local", capabilities_found=caps, scan_duration_ms=(time.perf_counter()-start)*1000, errors=errors)

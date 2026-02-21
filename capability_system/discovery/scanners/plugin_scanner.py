from __future__ import annotations

import json
import logging
import time
from pathlib import Path

from capability_system import config
from capability_system.discovery.scanners.base_scanner import BaseScanner
from capability_system.models.capability import Capability, CapabilityState, CapabilityType, ExecutionType, ResourceRequirements
from capability_system.models.discovery_result import DiscoveryResult


class PluginScanner(BaseScanner):
    scanner_name = "plugin_scanner"
    scanner_type = "plugin"

    def __init__(self, plugin_directory: str | None = None):
        self.plugin_directory = plugin_directory or config.PLUGIN_DIRECTORY
        self.logger = logging.getLogger("capability_system.discovery.plugin")

    def is_available(self) -> bool:
        return Path(self.plugin_directory).exists()

    def scan(self) -> DiscoveryResult:
        start = time.perf_counter()
        caps, errors = [], []
        root = Path(self.plugin_directory)
        for folder in root.iterdir() if root.exists() else []:
            manifest_file = folder / "manifest.json"
            if not manifest_file.exists():
                continue
            try:
                manifest = json.loads(manifest_file.read_text(encoding="utf-8"))
                entry_point = folder / manifest["entry_point"]
                if not entry_point.exists():
                    raise FileNotFoundError(f"Missing entry point {entry_point}")
                caps.append(Capability(name=manifest["name"], version=manifest["version"], capability_type=CapabilityType.PLUGIN, category=manifest.get("category", "data"), subcategory=manifest.get("subcategory", "processing"), description=manifest.get("description", ""), input_schema=manifest.get("input_schema", {}), output_schema=manifest.get("output_schema", {}), execution_endpoint=str(entry_point), execution_type=ExecutionType.PLUGIN, resource_requirements=ResourceRequirements(**manifest.get("resource_requirements", {})), dependencies=manifest.get("dependencies", []), metadata={"source":"local_scan","author":"","license":"","tags":["plugin"],"documentation_url":"","repository_url":""}, state=CapabilityState.DISCOVERED))
            except Exception as exc:
                errors.append(f"{folder.name}: {exc}")
        return DiscoveryResult(scanner_name=self.scanner_name, source_type="plugin", source_location=str(root), capabilities_found=caps, scan_duration_ms=(time.perf_counter()-start)*1000, errors=errors)

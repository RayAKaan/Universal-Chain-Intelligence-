from __future__ import annotations

import logging
import time

from capability_system import config
from capability_system.discovery.scanners.base_scanner import BaseScanner
from capability_system.models.capability import Capability, CapabilityState, CapabilityType, ExecutionType
from capability_system.models.discovery_result import DiscoveryResult

try:
    import requests
except Exception:  # noqa: BLE001
    requests = None


class APIScanner(BaseScanner):
    scanner_name = "api_scanner"
    scanner_type = "api"

    def __init__(self, endpoints: list[dict] | None = None):
        self.endpoints = endpoints if endpoints is not None else config.API_ENDPOINTS
        self.logger = logging.getLogger("capability_system.discovery.api")

    def is_available(self) -> bool:
        return True

    def scan(self) -> DiscoveryResult:
        start = time.perf_counter()
        caps, errors = [], []
        for api in self.endpoints:
            try:
                latency = 0.0
                health_url = api.get("health_check_url") or api["url"]
                if requests:
                    t0 = time.perf_counter(); resp = requests.get(health_url, timeout=config.API_REQUEST_TIMEOUT_SECONDS); latency = (time.perf_counter()-t0)*1000
                    if resp.status_code >= 400:
                        raise RuntimeError(f"API unhealthy {resp.status_code}")
                caps.append(Capability(name=api["name"], version="1.0.0", capability_type=CapabilityType.REST_API, category=api.get("category","network"), subcategory=api.get("subcategory","endpoint"), description=f"API endpoint {api['url']} latency={latency:.1f}ms", execution_endpoint=api["url"], execution_type=ExecutionType.API_CALL, execution_config={"method": api.get("method","GET")}, metadata={"source":"network","author":"","license":"","tags":["api"],"documentation_url":"","repository_url":""}, state=CapabilityState.DISCOVERED))
            except Exception as exc:
                errors.append(f"{api.get('name','unknown')}: {exc}")
        return DiscoveryResult(scanner_name=self.scanner_name, source_type="api", source_location="config", capabilities_found=caps, scan_duration_ms=(time.perf_counter()-start)*1000, errors=errors)

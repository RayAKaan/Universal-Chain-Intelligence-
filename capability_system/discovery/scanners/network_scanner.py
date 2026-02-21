from __future__ import annotations

import logging
import socket
import time

from capability_system import config
from capability_system.discovery.scanners.base_scanner import BaseScanner
from capability_system.models.capability import Capability, CapabilityState, CapabilityType, ExecutionType
from capability_system.models.discovery_result import DiscoveryResult


class NetworkScanner(BaseScanner):
    scanner_name = "network_scanner"
    scanner_type = "network"

    def __init__(self):
        self.logger = logging.getLogger("capability_system.discovery.network")

    def is_available(self) -> bool:
        return bool(config.NETWORK_SCAN_ENABLED)

    def scan(self) -> DiscoveryResult:
        start = time.perf_counter()
        caps, errors = [], []
        host = "127.0.0.1"
        for port in config.NETWORK_SCAN_PORTS:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(0.2)
            try:
                if sock.connect_ex((host, port)) == 0:
                    caps.append(Capability(name=f"service_{port}", version="1.0.0", capability_type=CapabilityType.REST_API, category="network", subcategory="service", description=f"Discovered local network service on {port}", execution_endpoint=f"http://{host}:{port}", execution_type=ExecutionType.API_CALL, metadata={"source":"network","author":"","license":"","tags":["network"],"documentation_url":"","repository_url":""}, state=CapabilityState.DISCOVERED))
            except Exception as exc:
                errors.append(str(exc))
            finally:
                sock.close()
        return DiscoveryResult(scanner_name=self.scanner_name, source_type="network", source_location=config.NETWORK_SCAN_RANGE, capabilities_found=caps, scan_duration_ms=(time.perf_counter()-start)*1000, errors=errors)

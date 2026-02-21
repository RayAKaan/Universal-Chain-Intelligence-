from __future__ import annotations

import importlib
import os
import shutil
import subprocess

from capability_system.models.capability import Capability, HealthStatus

try:
    import requests
except Exception:  # noqa: BLE001
    requests = None


def check_python_capability(capability: Capability) -> HealthStatus:
    try:
        endpoint = capability.execution_endpoint
        module = endpoint.split(":")[0] if ":" in endpoint else endpoint.split(".")[0]
        importlib.import_module(module)
        return HealthStatus.HEALTHY
    except Exception:
        return HealthStatus.UNHEALTHY


def check_shell_capability(capability: Capability) -> HealthStatus:
    try:
        binary = capability.execution_endpoint
        if shutil.which(binary) is None and not os.path.exists(binary):
            return HealthStatus.UNHEALTHY
        subprocess.run([binary, "--version"], capture_output=True, text=True, timeout=2, check=False)
        return HealthStatus.HEALTHY
    except Exception:
        return HealthStatus.DEGRADED


def check_api_capability(capability: Capability) -> HealthStatus:
    try:
        if not requests:
            return HealthStatus.UNKNOWN
        resp = requests.get(capability.execution_endpoint, timeout=5)
        if resp.status_code < 400:
            return HealthStatus.HEALTHY
        return HealthStatus.DEGRADED
    except Exception:
        return HealthStatus.UNHEALTHY


def check_model_capability(capability: Capability) -> HealthStatus:
    endpoint = capability.execution_endpoint
    if endpoint.startswith("http"):
        return check_api_capability(capability)
    return HealthStatus.HEALTHY if os.path.exists(endpoint) else HealthStatus.UNHEALTHY


def check_plugin_capability(capability: Capability) -> HealthStatus:
    return HealthStatus.HEALTHY if os.path.exists(capability.execution_endpoint) else HealthStatus.UNHEALTHY

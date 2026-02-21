from __future__ import annotations

from pathlib import Path
from urllib.parse import urlparse

from safety_system.scope.boundary_definitions import (
    ALLOWED_FILESYSTEM_PATHS,
    ALLOWED_NETWORK_DOMAINS,
    FORBIDDEN_COMMANDS,
    FORBIDDEN_FILESYSTEM_PATHS,
    MAX_RESOURCE_LIMITS,
)


class ScopeEnforcer:
    def __init__(self, boundary_definitions, scope_monitor, escalation_manager, config):
        self.monitor = scope_monitor
        self.escalation = escalation_manager

    def check_scope(self, action: str, target: str, context: dict) -> tuple[bool, str]:
        if action in {"read_file", "create_file", "delete_file"}:
            ok = self.is_within_filesystem_scope(target)
            reason = "filesystem scope check"
        elif action == "make_network_request":
            ok = self.is_within_network_scope(target)
            reason = "network scope check"
        elif action == "execute_shell_command":
            ok = self.is_within_execution_scope(target)
            reason = "execution scope check"
        else:
            ok, reason = True, "generic in-scope"
        self.monitor.record(action, ok, reason)
        if not ok:
            self.escalation.escalate(action, reason, "high")
        return ok, reason

    def is_within_filesystem_scope(self, path: str) -> bool:
        p = str(Path(path).as_posix())
        if any(p.startswith(x.rstrip("/")) for x in FORBIDDEN_FILESYSTEM_PATHS):
            return False
        return any(p.startswith(x.rstrip("/")) or p.startswith("./") for x in ALLOWED_FILESYSTEM_PATHS)

    def is_within_network_scope(self, url: str) -> bool:
        host = urlparse(url).hostname or ""
        return host in ALLOWED_NETWORK_DOMAINS

    def is_within_resource_scope(self, resource_request: dict) -> bool:
        return all(resource_request.get(k, 0) <= v for k, v in MAX_RESOURCE_LIMITS.items())

    def is_within_execution_scope(self, command: str) -> bool:
        low = command.lower()
        return not any(bad in low for bad in FORBIDDEN_COMMANDS)

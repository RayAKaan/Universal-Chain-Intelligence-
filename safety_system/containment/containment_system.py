from safety_system.models.containment_status import ContainmentStatus


class ContainmentSystem:
    def __init__(self, resource_boundaries, network_boundaries, filesystem_boundaries, execution_boundaries, config):
        self.resource = resource_boundaries
        self.network = network_boundaries
        self.filesystem = filesystem_boundaries
        self.execution = execution_boundaries
        self.monitor = []
        self._fs_v = 0
        self._nw_v = 0

    def check_containment(self) -> ContainmentStatus:
        intact = self._fs_v == 0 and self._nw_v == 0
        return ContainmentStatus(
            filesystem_contained=self._fs_v == 0,
            allowed_paths=["./", "data/"],
            filesystem_violations=self._fs_v,
            network_contained=self._nw_v == 0,
            allowed_domains=["pypi.org"],
            network_violations=self._nw_v,
            resource_contained=True,
            resource_limits=self.resource.limits(),
            current_usage={},
            execution_contained=True,
            blocked_operations=[],
            overall_containment="intact" if intact else "warning",
        )

    def is_contained(self) -> bool:
        return self.check_containment().overall_containment == "intact"

    def enforce_filesystem(self, path: str, operation: str) -> bool:
        ok = self.filesystem.is_allowed(path, operation)
        if not ok:
            self._fs_v += 1
        return ok

    def enforce_network(self, url: str, method: str) -> bool:
        ok = self.network.is_allowed(url, method)
        if not ok:
            self._nw_v += 1
        return ok

    def enforce_resource(self, resource: str, amount: float) -> bool:
        return self.resource.is_allowed(resource, amount)

    def enforce_execution(self, command: str) -> bool:
        return self.execution.is_allowed(command)

    def report_breach_attempt(self, boundary_type: str, details: dict) -> None:
        self.monitor.append({"boundary": boundary_type, "details": details})

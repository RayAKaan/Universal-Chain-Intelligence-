from safety_system.scope.boundary_definitions import FORBIDDEN_COMMANDS


class ExecutionBoundaries:
    def is_allowed(self, command: str) -> bool:
        low = command.lower()
        if any(c in low for c in ["sudo", " su "]):
            return False
        return not any(bad in low for bad in FORBIDDEN_COMMANDS)

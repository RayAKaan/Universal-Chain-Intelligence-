from safety_system.scope.boundary_definitions import MAX_RESOURCE_LIMITS


class ResourceBoundaries:
    def is_allowed(self, resource: str, amount: float) -> bool:
        return amount <= MAX_RESOURCE_LIMITS.get(resource, amount)

    def limits(self) -> dict:
        return dict(MAX_RESOURCE_LIMITS)

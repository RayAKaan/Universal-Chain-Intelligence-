class InterceptRegistry:
    def __init__(self):
        self._locked = False
        self._registry = {p: [] for p in ["phase0", "phase1", "phase2", "phase3", "phase4", "phase5"]}

    def register_first(self, phase: str, interceptor):
        if self._locked and self._registry[phase]:
            raise PermissionError("first interceptor immutable")
        if self._registry[phase]:
            self._registry[phase][0] = interceptor
        else:
            self._registry[phase].append(interceptor)

    def lock(self):
        self._locked = True

    def get(self, phase: str):
        return list(self._registry[phase])

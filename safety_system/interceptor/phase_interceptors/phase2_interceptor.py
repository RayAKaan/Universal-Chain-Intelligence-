class Phase2Interceptor:
    def __init__(self, central):
        self.central = central

    def intercept(self, action: str, source_component: str, target: str, payload: dict, context: dict):
        return self.central.intercept(action, "phase2", source_component, target, payload, context)

class ContainmentMonitor:
    def __init__(self):
        self.events = []

    def report(self, boundary_type: str, details: dict):
        self.events.append({"boundary": boundary_type, "details": details})

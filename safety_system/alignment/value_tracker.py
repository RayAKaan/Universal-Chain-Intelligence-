class ValueTracker:
    def __init__(self):
        self.events = []

    def record(self, dimensions: dict):
        self.events.append(dimensions)

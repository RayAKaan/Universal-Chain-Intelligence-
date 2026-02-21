class TrustHistory:
    def __init__(self):
        self.events = []

    def add(self, event: dict) -> None:
        self.events.append(event)

    def get(self) -> list[dict]:
        return list(self.events)

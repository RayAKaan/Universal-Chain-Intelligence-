class ReasoningRecorder:
    def __init__(self):
        self._store = {}

    def record(self, decision_id: str, reasoning_chain: list[str]) -> None:
        self._store[decision_id] = list(reasoning_chain)

    def get_reasoning(self, decision_id: str) -> list[str]:
        return self._store.get(decision_id, [])

    def search_reasoning(self, query: str) -> list[dict]:
        return [{"decision_id": k, "chain": v} for k, v in self._store.items() if query.lower() in " ".join(v).lower()]

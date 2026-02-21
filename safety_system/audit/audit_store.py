class AuditStore:
    def __init__(self):
        self._entries = []

    def append(self, entry):
        self._entries.append(entry)

    def all(self):
        return list(self._entries)

    def by_id(self, entry_id: str):
        for e in self._entries:
            if e.entry_id == entry_id:
                return e
        return None

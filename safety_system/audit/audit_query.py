class AuditQuery:
    def __init__(self, store):
        self.store = store

    def search(self, query: str):
        q = query.lower()
        return [e for e in self.store.all() if q in e.action.lower() or q in e.actor.lower() or q in e.target.lower()]

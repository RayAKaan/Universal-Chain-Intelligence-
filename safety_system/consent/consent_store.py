class ConsentStore:
    def __init__(self):
        self.records = []

    def add(self, rec):
        self.records.append(rec)

    def all(self):
        return list(self.records)

    def get(self, rec_id: str):
        for r in self.records:
            if r.record_id == rec_id:
                return r
        return None

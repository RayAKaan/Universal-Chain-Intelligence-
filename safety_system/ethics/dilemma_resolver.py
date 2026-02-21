class DilemmaResolver:
    def resolve(self, options: list[dict]) -> dict:
        return sorted(options, key=lambda o: o.get("risk", 1.0))[0] if options else {"decision": "defer"}

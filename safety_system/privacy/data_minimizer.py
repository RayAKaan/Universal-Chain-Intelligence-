class DataMinimizer:
    def minimize(self, data, purpose: str):
        if isinstance(data, dict):
            keys = [k for k in data if "id" in k or "status" in k or k == "result"]
            return {k: data[k] for k in keys} if keys else {"summary": "minimized"}
        return str(data)[:200]

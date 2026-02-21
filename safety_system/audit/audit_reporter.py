class AuditReporter:
    def report(self, entries: list) -> str:
        lines = ["Audit Trail"]
        lines.extend([f"{e.sequence_number}: {e.action} => {e.outcome}" for e in entries])
        return "\n".join(lines)

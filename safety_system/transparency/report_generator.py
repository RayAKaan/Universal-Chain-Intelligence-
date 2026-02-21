class ReportGenerator:
    def generate(self, decisions: list) -> str:
        lines = ["Transparency Report"]
        for d in decisions:
            lines.append(f"- {d.timestamp.isoformat()} | {d.action_requested} | {d.decision}")
        return "\n".join(lines)

class AlignmentReport:
    def render(self, score, drift: dict) -> str:
        return f"Alignment {score.overall_score:.2f} ({score.trend}) | drift={drift['severity']}"

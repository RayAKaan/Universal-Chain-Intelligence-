from safety_system.models.alignment_score import AlignmentScore


class AlignmentMonitor:
    def __init__(self, alignment_scorer, drift_detector, value_tracker):
        self.scorer = alignment_scorer
        self.detector = drift_detector
        self.value_tracker = value_tracker
        self.history = []

    def monitor(self) -> AlignmentScore:
        scored = self.scorer.score({})
        trend = "stable"
        if self.history and scored["overall"] > self.history[-1].overall_score:
            trend = "improving"
        score = AlignmentScore(overall_score=scored["overall"], dimension_scores=scored["dimensions"], trend=trend)
        self.history.append(score)
        self.value_tracker.record(scored["dimensions"])
        return score

    def check_drift(self) -> dict:
        current = self.history[-1] if self.history else self.monitor()
        return self.detector.detect(current, self.history[:-1])

    def get_alignment_history(self):
        return list(self.history)

    def get_current_score(self):
        return self.history[-1] if self.history else self.monitor()

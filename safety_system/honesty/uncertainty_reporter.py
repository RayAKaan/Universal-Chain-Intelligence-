class UncertaintyReporter:
    def annotate(self, text: str, confidence: float) -> str:
        return text if confidence >= 0.8 else f"{text} (uncertainty noted: confidence={confidence:.2f})"

class SocialEngineeringDetector:
    def detect(self, text: str) -> tuple[bool, list[str]]:
        markers = ["trust me", "no one will know", "secretly", "don't tell"]
        hits = [m for m in markers if m in text.lower()]
        return not hits, hits

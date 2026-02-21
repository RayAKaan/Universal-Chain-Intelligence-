TONE_GUIDELINES = {
    "greeting": "warm, welcoming",
    "acknowledgment": "enthusiastic, supportive",
    "progress": "encouraging, informative",
    "completion": "celebratory, summarizing",
    "error": "apologetic, helpful, constructive",
    "denial": "understanding, explanatory, offering alternatives",
    "warning": "caring, clear, non-alarming",
    "emergency": "calm, authoritative, reassuring",
}


class ToneManager:
    def apply_tone(self, message: str, tone_type: str) -> str:
        return f"[{tone_type}] {message}"

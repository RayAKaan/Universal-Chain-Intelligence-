class CommunicationValidator:
    def validate(self, text: str) -> tuple[bool, list[str]]:
        issues = ["deceptive_phrase"] if "definitely" in text.lower() and "uncertain" in text.lower() else []
        return not issues, issues

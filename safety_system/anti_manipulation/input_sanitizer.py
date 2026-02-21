import re


class InputSanitizer:
    def sanitize(self, input_text: str) -> str:
        text = input_text.encode("utf-8", "ignore").decode("utf-8")
        text = re.sub(r"[\x00-\x1f]", "", text)
        return text.strip()

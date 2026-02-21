class DataClassifier:
    def classify(self, data) -> str:
        text = str(data).lower()
        if any(k in text for k in ["password", "ssn", "private key"]):
            return "sensitive"
        if any(k in text for k in ["email", "phone", "address"]):
            return "personal"
        return "internal"

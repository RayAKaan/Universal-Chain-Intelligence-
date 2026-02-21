from safety_system.privacy.privacy_policies import PRIVACY_POLICIES


class PrivacyGuardian:
    def __init__(self, data_classifier, data_minimizer, access_controller):
        self.classifier = data_classifier
        self.minimizer = data_minimizer
        self.access = access_controller

    def check_privacy(self, action: str, data) -> tuple[bool, list[str]]:
        c = self.classifier.classify(data)
        issues = []
        if c in {"personal", "sensitive"} and "send" in action.lower():
            issues.append("possible data exfiltration")
        return not issues, issues

    def classify_data(self, data) -> str:
        return self.classifier.classify(data)

    def minimize_data(self, data, purpose: str):
        return self.minimizer.minimize(data, purpose)

    def check_data_retention(self, data_type: str) -> dict:
        return PRIVACY_POLICIES.get(data_type, PRIVACY_POLICIES["internal"])

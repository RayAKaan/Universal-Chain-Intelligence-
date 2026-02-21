class HonestyEnforcer:
    def __init__(self, communication_validator, claim_verifier, uncertainty_reporter):
        self.validator = communication_validator
        self.claims = claim_verifier
        self.uncertainty = uncertainty_reporter

    def enforce(self, text: str, confidence: float = 1.0) -> tuple[bool, str, list[str]]:
        ok1, issues1 = self.validator.validate(text)
        ok2, issues2 = self.claims.verify_claims(text)
        msg = self.uncertainty.annotate(text, confidence)
        issues = issues1 + issues2
        return ok1 and ok2, msg, issues

class BypassDetector:
    def detect_bypass_attempt(self, operation: dict) -> bool:
        return operation.get("interceptor_used") is False or operation.get("direct_phase_call") is True

class AccessController:
    def check_access(self, component: str, data_type: str, operation: str) -> bool:
        if data_type in {"personal", "sensitive"} and component not in {"privacy_guardian", "consent_manager"}:
            return False
        return True

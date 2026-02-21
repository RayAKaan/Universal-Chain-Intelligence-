PRIVACY_POLICIES = {
    "public": {"retention_days": 365, "allow_export": True},
    "internal": {"retention_days": 180, "allow_export": False},
    "confidential": {"retention_days": 90, "allow_export": False},
    "personal": {"retention_days": 30, "allow_export": False},
    "sensitive": {"retention_days": 7, "allow_export": False},
}

STRICT_POLICY = {"require_for": ["CAUTION", "RISKY", "DANGEROUS"], "blanket": False}
BALANCED_POLICY = {"require_for": ["RISKY", "DANGEROUS"], "blanket_caution": True, "blanket_ttl": 3600}
PERMISSIVE_POLICY = {"require_for": ["DANGEROUS"], "blanket_risky": True}

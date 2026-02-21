import hashlib


def fingerprint(data: str) -> str:
    return hashlib.sha256(data.encode("utf-8")).hexdigest()[:16]


def require_keys(payload: dict, keys: list[str]) -> tuple[bool, list[str]]:
    missing = [k for k in keys if k not in payload]
    return not missing, missing

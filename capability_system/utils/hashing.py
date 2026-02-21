from __future__ import annotations

import hashlib
import uuid


def generate_id() -> str:
    return str(uuid.uuid4())


def generate_fingerprint(capability) -> str:
    raw = f"{capability.name}|{capability.version}|{capability.execution_endpoint}|{capability.execution_type}"
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()

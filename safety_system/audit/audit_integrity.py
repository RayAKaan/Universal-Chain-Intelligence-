from safety_system.utils.crypto_utils import sha256_text


def calculate_entry_hash(entry) -> str:
    base = f"{entry.sequence_number}|{entry.timestamp.isoformat()}|{entry.action}|{entry.actor}|{entry.target}|{entry.outcome}|{entry.previous_hash}"
    return sha256_text(base)


def verify_chain(entries: list) -> bool:
    return len(detect_tampering(entries)) == 0


def detect_tampering(entries: list) -> list[str]:
    issues = []
    for i, entry in enumerate(entries):
        if i > 0 and entry.previous_hash != entries[i - 1].entry_hash:
            issues.append(f"hash link mismatch at seq {entry.sequence_number}")
        if calculate_entry_hash(entry) != entry.entry_hash:
            issues.append(f"entry hash mismatch at seq {entry.sequence_number}")
        if i > 0 and entry.sequence_number != entries[i - 1].sequence_number + 1:
            issues.append(f"sequence gap at seq {entry.sequence_number}")
    return issues

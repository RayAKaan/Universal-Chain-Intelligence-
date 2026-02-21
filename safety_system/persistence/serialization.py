import json
from dataclasses import asdict, is_dataclass


def to_json(data) -> str:
    if is_dataclass(data):
        data = asdict(data)
    return json.dumps(data, default=str, sort_keys=True)

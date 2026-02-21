from __future__ import annotations
import json
from dataclasses import asdict, is_dataclass
from datetime import datetime
from enum import Enum

def _default(o):
    if isinstance(o,datetime): return o.isoformat()
    if isinstance(o,Enum): return o.value
    if is_dataclass(o): return asdict(o)
    return str(o)
def serialize(obj): return json.dumps(obj,default=_default)
def deserialize(data): return json.loads(data) if data else {}

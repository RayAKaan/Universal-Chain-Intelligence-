from __future__ import annotations
import json
from dataclasses import asdict, is_dataclass
from datetime import datetime
from enum import Enum
def _d(o):
    if isinstance(o,datetime): return o.isoformat()
    if isinstance(o,Enum): return o.value
    if is_dataclass(o): return asdict(o)
    return str(o)
def dumps(o): return json.dumps(o,default=_d)
def loads(s): return json.loads(s) if s else {}
